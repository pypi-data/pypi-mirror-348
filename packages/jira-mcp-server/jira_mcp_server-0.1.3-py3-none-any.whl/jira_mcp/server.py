from typing import Any, Literal

from pydantic import Field

from fastmcp import Context, FastMCP
from fastmcp.utilities.logging import get_logger

from jira_mcp.jira_client import JiraClient

logger = get_logger(__name__)

# Initialize the MCP Server
mcp = FastMCP(
    name="Jira Integration Server",
    instructions="""
    This server interacts with a Jira instance.
    Use 'jira_client_init' first if you encounter connection issues.
    Tools available: get issue details, update issues, transition issues, create issues, add comments, download attachments, list issue types.
    """,
    dependencies=[],
    # Add dependencies required by the client and server itself if packaging
    # dependencies=["jira-mcp-server @ file://..."], # Example if local package
)

# Create a single JiraClient instance for the server lifecycle
# Connection will be established lazily on first tool use or explicit init
jira_client = JiraClient()

# --- Tools ---

@mcp.tool()
async def jira_client_init() -> str:
    """
    Explicitly initializes the connection to the Jira instance using configured credentials.
    Useful to call first if other tools report connection errors.
    Returns the connection status and authentication method used.
    """
    logger.info("Explicitly initializing Jira client via tool call.")
    try:
        status = await jira_client.initialize()
        return f"Initialization successful: {status}"
    except ConnectionError as e:
        logger.error(f"Explicit initialization failed: {e}")
        return f"Error: Jira connection failed - {e}"
    except Exception as e:
         logger.error(f"Unexpected error during explicit initialization: {e}")
         return f"Error: An unexpected error occurred during Jira initialization: {e}"

@mcp.tool()
async def jira_get_issue(
    issue_key: str = Field(..., description="The key of the Jira issue (e.g., 'PROJ-123')."),
    fields: list[str] | None = Field(None, description="Specific fields to retrieve (comma-separated string or list). Defaults to all fields."),
    expand: list[str] | None = Field(None, description="Fields to expand (e.g., 'changelog', 'renderedFields').")
) -> dict[str, Any]:
    """Retrieves details for a specific Jira issue by its key."""
    fields_str = ",".join(fields) if fields else None
    expand_str = ",".join(expand) if expand else None
    try:
        issue_data = await jira_client.get_issue(issue_key, fields=fields_str, expand=expand_str)
        return issue_data
    except Exception as e:
        return {"error": f"Failed to get issue {issue_key}: {e}"}

@mcp.tool()
async def jira_get_batch_issues(
    issue_keys: list[str] = Field(..., description="A list of Jira issue keys (e.g., ['PROJ-123', 'PROJ-124'])."),
    fields: list[str] | None = Field(None, description="Specific fields to retrieve for each issue."),
    expand: list[str] | None = Field(None, description="Fields to expand for each issue.")
) -> list[dict[str, Any]]:
    """Retrieves details for multiple Jira issues by their keys in a single request."""
    if not issue_keys:
        return []
    fields_str = ",".join(fields) if fields else None
    expand_str = ",".join(expand) if expand else None
    try:
        # Note: The client method handles JQL internally now
        issues_data = await jira_client.get_batch_issues(issue_keys, fields=fields_str, expand=expand_str)
        return issues_data
    except Exception as e:
        return [{"error": f"Failed to get batch issues: {e}"}]


@mcp.tool()
async def jira_update_issue(
    issue_key: str = Field(..., description="The key of the Jira issue to update (e.g., 'PROJ-123')."),
    summary: str | None = Field(None, description="New summary for the issue."),
    description: str | None = Field(None, description="New description for the issue."),
    assignee_name: str | None = Field(None, description="Username of the new assignee. Use 'null' or an empty string to unassign."),
    priority_name: str | None = Field(None, description="Name of the new priority (e.g., 'High', 'Medium')."),
    labels: list[str] | None = Field(None, description="New list of labels (replaces existing labels)."),
    add_labels: list[str] | None = Field(None, description="List of labels to add."),
    remove_labels: list[str] | None = Field(None, description="List of labels to remove."),
    custom_fields: dict[str, Any] | None = Field(None, description="Dictionary of custom field updates (e.g., {'customfield_10010': 'value'})."),
    comment: str | None = Field(None, description="Add a comment during the update."),
) -> dict[str, Any]:
    """Updates fields of an existing Jira issue. Can also add a comment."""
    fields_to_update = {}
    update_operations = {} # For operations like add/remove labels

    if summary is not None:
        fields_to_update["summary"] = summary
    if description is not None:
        fields_to_update["description"] = description
    if assignee_name is not None:
        # Handle unassignment:jira library expects None for the value part of the dict
        fields_to_update["assignee"] = {"name": assignee_name} if assignee_name else None
    if priority_name is not None:
        fields_to_update["priority"] = {"name": priority_name}
    if labels is not None: # This replaces all existing labels
        fields_to_update["labels"] = labels
    if custom_fields:
        fields_to_update.update(custom_fields)

    # Handle label additions/removals using the 'update' field
    label_ops = []
    if add_labels:
        label_ops.extend([{"add": lbl} for lbl in add_labels])
    if remove_labels:
         label_ops.extend([{"remove": lbl} for lbl in remove_labels])
    if label_ops and "labels" not in fields_to_update: # Don't combine set and add/remove in one request
        update_operations["labels"] = label_ops

    if comment:
        if "comment" not in update_operations:
            update_operations["comment"] = []
        update_operations["comment"].append({"add": {"body": comment}})


    if not fields_to_update and not update_operations:
        return {"error": "No fields or update operations provided for update.", "success": False}

    try:
        success = await jira_client.update_issue(issue_key, fields=fields_to_update or None, update=update_operations or None)
        if success:
            return {"message": f"Issue {issue_key} updated successfully.", "success": True}
        else:
            # The jira library update might return False for various reasons not raising exceptions
             return {"error": f"Failed to update issue {issue_key}. Jira API returned non-success, but no error was raised.", "success": False}
    except Exception as e:
        return {"error": f"Failed to update issue {issue_key}: {e}", "success": False}

@mcp.tool()
async def jira_get_transitions(
    issue_key: str = Field(..., description="The key of the Jira issue (e.g., 'PROJ-123').")
) -> list[dict[str, Any]]:
    """Retrieves the available status transitions for a specific Jira issue."""
    try:
        transitions = await jira_client.get_transitions(issue_key)
        # Format for better readability
        return [{"id": t['id'], "name": t['name'], "to_status": t['to']['name']} for t in transitions]
    except Exception as e:
        return [{"error": f"Failed to get transitions for {issue_key}: {e}"}]

@mcp.tool()
async def jira_transition_issue(
    issue_key: str = Field(..., description="The key of the Jira issue to transition (e.g., 'PROJ-123')."),
    transition: str = Field(..., description="The ID or Name of the transition to execute (e.g., '5' or 'Resolve Issue')."),
    resolution_name: str | None = Field(None, description="Required resolution name for transitions like 'Done' or 'Resolved' (e.g., 'Fixed', 'Done')."),
    comment: str | None = Field(None, description="Optional comment to add during the transition."),
    assignee_name: str | None = Field(None, description="Optional username to assign the issue to during transition."),
    custom_fields: dict[str, Any] | None = Field(None, description="Dictionary of custom field values required by the transition screen."),
) -> dict[str, Any]:
    """Transitions a Jira issue to a different status using a transition ID or name."""
    fields = {}
    if resolution_name:
        fields["resolution"] = {"name": resolution_name}
    if assignee_name:
        fields["assignee"] = {"name": assignee_name}
    if custom_fields:
        fields.update(custom_fields)

    try:
        await jira_client.transition_issue(
            issue_key,
            transition,
            fields=fields or None,
            comment=comment
        )
        return {"message": f"Issue {issue_key} transitioned successfully using '{transition}'.", "success": True}
    except Exception as e:
        return {"error": f"Failed to transition issue {issue_key}: {e}", "success": False}


@mcp.tool()
async def jira_download_attachments(
    issue_key: str = Field(..., description="The key of the Jira issue (e.g., 'PROJ-123')."),
    target_dir: str = Field(".", description="Directory path where attachments should be saved. Defaults to the current directory.")
) -> dict[str, Any]:
    """Downloads all attachments from a specific Jira issue to a local directory."""
    try:
        downloaded_files = await jira_client.download_attachments(issue_key, target_dir)
        if downloaded_files:
            return {
                "message": f"Successfully downloaded {len(downloaded_files)} attachments for {issue_key} to {target_dir}.",
                "downloaded_files": downloaded_files,
                "success": True
            }
        else:
            return {"message": f"No attachments found for {issue_key} or download failed.", "success": True} # Considered success if no attachments
    except Exception as e:
        return {"error": f"Failed to download attachments for {issue_key}: {e}", "success": False}

@mcp.tool()
async def jira_create_issue(
    project_key: str = Field(..., description="The key of the project (e.g., 'PROJ')."),
    summary: str = Field(..., description="A concise summary of the issue."),
    issuetype_name: str = Field(..., description="The name of the issue type (e.g., 'Bug', 'Task', 'Story'). Use 'jira_get_project_issue_types' to find available types."),
    description: str | None = Field(None, description="Detailed description of the issue."),
    assignee_name: str | None = Field(None, description="Username of the person to assign the issue to."),
    priority_name: str | None = Field(None, description="Name of the priority (e.g., 'High', 'Medium', 'Lowest')."),
    labels: list[str] | None = Field(None, description="List of labels to add to the issue."),
    custom_fields: dict[str, Any] | None = Field(None, description="Dictionary of custom fields (e.g., {'customfield_10010': 'value'}). Use field IDs."),
) -> dict[str, Any]:
    """Creates a new issue in a specified Jira project."""
    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "issuetype": {"name": issuetype_name},
    }
    if description:
        fields["description"] = description
    if assignee_name:
        fields["assignee"] = {"name": assignee_name}
    if priority_name:
        fields["priority"] = {"name": priority_name}
    if labels:
        fields["labels"] = labels
    if custom_fields:
        fields.update(custom_fields)

    try:
        new_issue_data = await jira_client.create_issue(fields)
        return {
            "message": f"Successfully created issue {new_issue_data['key']}.",
            "issue_key": new_issue_data['key'],
            "issue_id": new_issue_data['id'],
            "issue_url": f"{jira_client.base_url}/browse/{new_issue_data['key']}",
            "success": True
         }
    except Exception as e:
        return {"error": f"Failed to create issue: {e}", "success": False}

@mcp.tool()
async def jira_get_project_issue_types(
    project_key: str = Field(..., description="The key of the project (e.g., 'PROJ').")
) -> list[dict[str, Any]]:
    """Retrieves the available issue types for a specific Jira project."""
    try:
        issue_types = await jira_client.get_project_issue_types(project_key)
        return issue_types
    except Exception as e:
        return [{"error": f"Failed to get issue types for project {project_key}: {e}"}]

@mcp.tool()
async def jira_add_comment(
    issue_key: str = Field(..., description="The key of the Jira issue (e.g., 'PROJ-123')."),
    body: str = Field(..., description="The content of the comment."),
    visibility_type: Literal["role", "group"] | None = Field(None, description="Set comment visibility to 'role' or 'group'."),
    visibility_value: str | None = Field(None, description="The name of the role or group for visibility.")
) -> dict[str, Any]:
    """Adds a comment to a specific Jira issue."""
    visibility = None
    if visibility_type and visibility_value:
        visibility = {"type": visibility_type, "value": visibility_value}
    elif visibility_type or visibility_value:
         return {"error": "Both visibility_type and visibility_value must be provided if setting visibility.", "success": False}

    try:
        comment_data = await jira_client.add_comment(issue_key, body, visibility=visibility)
        return {
            "message": f"Comment added successfully to {issue_key}.",
            "comment_id": comment_data['id'],
            "success": True
        }
    except Exception as e:
        return {"error": f"Failed to add comment to {issue_key}: {e}", "success": False}

# Optional: Add lifespan management if needed (e.g., to close client properly)
# @asynccontextmanager
# async def lifespan(app: FastMCP):
#     # Startup logic if needed
#     yield
#     # Shutdown logic
#     await jira_client.close()

# mcp.lifespan = lifespan # Assign if you define a lifespan context manager