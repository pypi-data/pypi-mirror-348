import base64
import os
import re
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import anyio
import httpx
from jira import JIRA, JIRAError
from jira.resources import Attachment

from fastmcp.utilities.logging import get_logger

from .settings import settings

logger = get_logger("jira_client")

class JiraClient:
    """
    Asynchronous client for interacting with the Jira API using Basic Auth or Session Auth.
    Handles initialization and common Jira operations.
    """

    def __init__(self):
        self._client: JIRA | None = None
        self._initialized = False
        self._auth_method_used: str | None = None
        self.base_url = str(settings.base_url).rstrip('/') # Ensure no trailing slash

        # Use httpx client for downloads as jira lib doesn't handle async downloads well
        self._httpx_client: httpx.AsyncClient | None = None

    async def _initialize_httpx_client(self):
        """Initializes the httpx client with appropriate auth."""
        if self._httpx_client:
            return

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        cookies = {}
        auth = None

        if self._auth_method_used == "session":
            cookies = {"JSESSIONID": settings.session_id}
            logger.debug("Initializing httpx client with Session ID cookie.")
        elif self._auth_method_used == "basic":
            auth = httpx.BasicAuth(settings.username, settings.password) # type: ignore
            logger.debug("Initializing httpx client with Basic Auth.")
        # No else needed, auth will remain None if no method used yet (shouldn't happen after init)

        self._httpx_client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            cookies=cookies, # type: ignore
            auth=auth,
            timeout=30.0, # Sensible default timeout
            follow_redirects=True,
        )

    async def initialize(self) -> str:
        """
        Initializes the Jira client connection using configured credentials.
        Prioritizes Session ID, then falls back to Basic Auth.

        Returns:
            str: A message indicating the connection status and auth method used.

        Raises:
            ConnectionError: If connection or authentication fails.
        """
        if self._initialized and self._client:
            logger.debug(f"Jira client already initialized with {self._auth_method_used} auth.")
            return f"Already connected to {self.base_url} using {self._auth_method_used} auth."

        logger.info(f"Attempting to initialize Jira connection to {self.base_url}")
        auth_details = None
        cookies = None
        auth_method = "None"

        # 1. Try Session ID if available
        if settings.has_session_auth:
            logger.debug("Attempting connection using JIRA_SESSION_ID.")
            try:
                # Need cookies dict for JIRA library
                cookies = {"JSESSIONID": settings.session_id}
                options = {"server": self.base_url}
                
                # Create a helper function to initialize JIRA with cookies
                def create_jira_with_cookies():
                    return JIRA(options, cookies=cookies)
                
                jira = await anyio.to_thread.run_sync(
                    create_jira_with_cookies, cancellable=True
                )
                # Verify connection by getting server info
                await anyio.to_thread.run_sync(jira.server_info, cancellable=True)
                self._client = jira
                self._initialized = True
                self._auth_method_used = "session"
                await self._initialize_httpx_client() # Init httpx client with session
                logger.info(f"Successfully connected to Jira using Session ID.")
                return f"Connected to {self.base_url} using Session ID."
            except JIRAError as e:
                logger.warning(f"Session ID connection failed (Status: {e.status_code}): {e.text}. Falling back...")
            except Exception as e:
                logger.warning(f"Session ID connection failed unexpectedly: {e}. Falling back...")

        # 2. Try Basic Auth if available (and session failed or wasn't tried)
        if settings.has_basic_auth:
            logger.debug("Attempting connection using JIRA_USERNAME/JIRA_PASSWORD.")
            try:
                auth_details = (settings.username, settings.password)
                options = {"server": self.base_url}
                
                # Create a helper function to initialize JIRA with basic_auth
                def create_jira_with_basic_auth():
                    return JIRA(options, basic_auth=auth_details)
                
                jira = await anyio.to_thread.run_sync(
                    create_jira_with_basic_auth, cancellable=True
                )
                
                # Verify connection by getting server info
                await anyio.to_thread.run_sync(jira.server_info, cancellable=True)
                self._client = jira
                self._initialized = True
                self._auth_method_used = "basic"
                await self._initialize_httpx_client() # Init httpx client with basic auth
                logger.info(f"Successfully connected to Jira using Basic Auth.")
                return f"Connected to {self.base_url} using Basic Auth."
            except JIRAError as e:
                logger.error(f"Basic Auth connection failed (Status: {e.status_code}): {e.text}")
                raise ConnectionError(f"Jira connection failed using Basic Auth: {e.text} (Status: {e.status_code})") from e
            except Exception as e:
                 logger.error(f"Basic Auth connection failed unexpectedly: {e}")
                 raise ConnectionError(f"Jira connection failed unexpectedly using Basic Auth: {e}") from e

        # 3. If neither worked
        logger.error("Jira initialization failed: No valid authentication method succeeded.")
        raise ConnectionError("Could not connect to Jira. Check credentials and base URL.")

    async def ensure_initialized(self):
        """Ensures the client is initialized before making a request."""
        if not self._initialized or not self._client:
            await self.initialize()
        if not self._client: # Should not happen if initialize succeeded
             raise RuntimeError("Jira client is not initialized.")
        if not self._httpx_client: # Should have been initialized with the client
            await self._initialize_httpx_client()
        if not self._httpx_client:
            raise RuntimeError("HTTPX client is not initialized.")


    async def _run_sync[T](self, func, *args, **kwargs) -> T:
        """Helper to run synchronous jira-python calls in a thread."""
        await self.ensure_initialized()
        try:
            # Pass the initialized client's session if available for subsequent calls
            # This helps maintain the session state established during initialization.
            options = {}
            if hasattr(self._client, 'options'):
                options = self._client.options # type: ignore

            # Use functools.partial to wrap the function call with its arguments
            from functools import partial
            sync_call = partial(func, *args, **kwargs)

            # Execute the synchronous call in a separate thread
            result = await anyio.to_thread.run_sync(sync_call, cancellable=True)
            return result
        except JIRAError as e:
            logger.error(f"Jira API error ({e.status_code}): {e.text}", exc_info=True)
            # Try to extract more specific error messages
            error_details = e.text
            try:
                error_json = json.loads(e.text)
                messages = error_json.get('errorMessages', [])
                errors = error_json.get('errors', {})
                if messages:
                    error_details = "; ".join(messages)
                if errors:
                    error_details += " Fields: " + json.dumps(errors)
            except json.JSONDecodeError:
                pass # Keep original text if not JSON

            # Re-raise with a more descriptive message, possibly wrapping specific types
            if e.status_code == 401:
                 raise PermissionError(f"Jira Authentication Error: {error_details}") from e
            elif e.status_code == 403:
                raise PermissionError(f"Jira Permission Denied: {error_details}") from e
            elif e.status_code == 404:
                raise ValueError(f"Jira Resource Not Found: {error_details}") from e
            else:
                raise ValueError(f"Jira API Error ({e.status_code}): {error_details}") from e
        except Exception as e:
            logger.error(f"Unexpected error during Jira operation: {e}", exc_info=True)
            raise RuntimeError(f"An unexpected error occurred: {e}") from e

    # --- API Methods ---

    async def get_issue(self, issue_key: str, fields: str | None = None, expand: str | None = None) -> dict[str, Any]:
        """Retrieves a Jira issue by its key."""
        logger.info(f"Fetching issue: {issue_key}")
        issue = await self._run_sync(self._client.issue, issue_key, fields=fields, expand=expand) # type: ignore
        return issue.raw # Return the raw dictionary representation

    async def get_batch_issues(self, issue_keys: list[str], fields: str | None = None, expand: str | None = None) -> list[dict[str, Any]]:
        """Retrieves multiple Jira issues by their keys using JQL."""
        if not issue_keys:
            return []
        jql = f"key in ({','.join(issue_keys)})"
        logger.info(f"Fetching batch issues with JQL: {jql}")
        search_params = {
            "jql_str": jql,
            "fields": fields,
            "expand": expand,
            "maxResults": len(issue_keys), # Ensure we get all requested issues if they exist
        }
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        results = await self._run_sync(self._client.search_issues, **search_params) # type: ignore
        return [issue.raw for issue in results]


    async def update_issue(self, issue_key: str, fields: dict[str, Any] | None = None, update: dict[str, Any] | None = None) -> bool:
        """Updates an existing Jira issue."""
        logger.info(f"Updating issue: {issue_key}")
        issue = await self._run_sync(self._client.issue, issue_key) # type: ignore
        # The update method returns True on success, False otherwise
        # We pass notify=False to avoid Jira sending email notifications
        success = await self._run_sync(issue.update, fields=fields, update=update, notify=False) # type: ignore
        logger.info(f"Update result for {issue_key}: {success}")
        return success

    async def transition_issue(self, issue_key: str, transition: str | dict[str, Any], fields: dict[str, Any] | None = None, comment: str | None = None) -> bool:
        """Transitions a Jira issue to a new status."""
        logger.info(f"Transitioning issue {issue_key} with transition: {transition}")
        # transition can be transition ID (str) or name (str) or a dict like {'id': '5'}
        success = await self._run_sync(
            self._client.transition_issue, # type: ignore
            issue_key,
            transition,
            fields=fields,
            comment=comment
        )
        logger.info(f"Transition result for {issue_key}: {success}")
        return success

    async def get_transitions(self, issue_key: str) -> list[dict[str, Any]]:
        """Gets available transitions for a Jira issue."""
        logger.info(f"Getting transitions for issue: {issue_key}")
        transitions = await self._run_sync(self._client.transitions, issue_key) # type: ignore
        # transitions returns a list of dicts like [{'id': '5', 'name': 'Resolve Issue', ...}]
        return transitions

    async def get_attachments(self, issue_key: str) -> list[dict[str, Any]]:
        """Gets attachments for a Jira issue."""
        logger.info(f"Getting attachments for issue: {issue_key}")
        issue = await self._run_sync(self._client.issue, issue_key, fields="attachment") # type: ignore
        attachments = getattr(issue.fields, 'attachment', [])
        return [att.raw for att in attachments] # Return raw dicts

    async def download_attachments(self, issue_key: str, target_dir: str | Path) -> list[str]:
        """Downloads all attachments for a given issue to the target directory."""
        logger.info(f"Downloading attachments for {issue_key} to {target_dir}")
        await self.ensure_initialized()
        target_path = Path(target_dir).resolve()
        target_path.mkdir(parents=True, exist_ok=True)

        attachments_data = await self.get_attachments(issue_key)
        if not attachments_data:
            logger.info(f"No attachments found for issue {issue_key}.")
            return []

        downloaded_files = []
        async with anyio.create_task_group() as tg:
            for att_data in attachments_data:
                attachment = Attachment(options={'server': self.base_url}, session=self._client.session, raw=att_data) # type: ignore
                # Sanitize filename
                filename = re.sub(r'[\\/*?:"<>|]', "_", attachment.filename)
                filepath = target_path / filename
                # Use httpx client for async download
                tg.start_soon(self._download_single_attachment_httpx, attachment.content, filepath, downloaded_files)

        logger.info(f"Finished downloading {len(downloaded_files)} attachments for {issue_key}.")
        return [str(p) for p in downloaded_files]

    async def _download_single_attachment_httpx(self, url: str, filepath: Path, downloaded_files_list: list):
        """Helper to download a single attachment using httpx."""
        if not self._httpx_client:
             raise RuntimeError("HTTPX client not initialized for download.")
        try:
            logger.debug(f"Starting download: {url} -> {filepath}")
            async with self._httpx_client.stream("GET", url) as response:
                response.raise_for_status() # Check for HTTP errors
                async with await anyio.open_file(filepath, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        await f.write(chunk)
            logger.debug(f"Finished download: {filepath}")
            downloaded_files_list.append(filepath)
        except httpx.HTTPStatusError as e:
             logger.error(f"HTTP error downloading {url}: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"Error downloading attachment {url} to {filepath}: {e}", exc_info=True)


    async def create_issue(self, fields: dict[str, Any]) -> dict[str, Any]:
        """Creates a new Jira issue."""
        logger.info(f"Creating issue with fields: {fields}")
        # The create_issue method returns the created Issue object
        new_issue = await self._run_sync(self._client.create_issue, fields=fields) # type: ignore
        logger.info(f"Issue created successfully: {new_issue.key}")
        return new_issue.raw

    async def get_project_issue_types(self, project_key: str) -> list[dict[str, Any]]:
         """Gets available issue types for a specific project."""
         logger.info(f"Getting issue types for project: {project_key}")
         # The createmeta endpoint provides this information
         # It's structured deeply, so we navigate to the relevant part
         meta = await self._run_sync(self._client.createmeta, projectKeys=project_key, expand="projects.issuetypes.fields") # type: ignore

         project_meta = next((p for p in meta.get('projects', []) if p.get('key') == project_key), None)
         if not project_meta:
             raise ValueError(f"Project '{project_key}' not found or no metadata available.")

         issue_types = project_meta.get('issuetypes', [])
         # Return relevant details for each issue type
         return [
             {
                 "id": it.get("id"),
                 "name": it.get("name"),
                 "description": it.get("description"),
                 "subtask": it.get("subtask", False),
                 # Optionally include available fields if needed: 'fields': it.get('fields')
             }
             for it in issue_types
         ]


    async def add_comment(self, issue_key: str, body: str, visibility: dict[str, str] | None = None) -> dict[str, Any]:
        """Adds a comment to a Jira issue."""
        logger.info(f"Adding comment to issue: {issue_key}")
        # The add_comment method returns the created Comment object
        comment = await self._run_sync(self._client.add_comment, issue_key, body, visibility=visibility) # type: ignore
        logger.info(f"Comment added successfully to {issue_key}: ID {comment.id}")
        return comment.raw

    async def close(self):
        """Closes the Jira client session and the httpx client."""
        if self._client:
            logger.info("Closing Jira client session.")
            await anyio.to_thread.run_sync(self._client.close) # type: ignore
            self._client = None
        if self._httpx_client:
             logger.info("Closing httpx client.")
             await self._httpx_client.aclose()
             self._httpx_client = None
        self._initialized = False
        self._auth_method_used = None

    async def __aenter__(self):
        await self.ensure_initialized()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()