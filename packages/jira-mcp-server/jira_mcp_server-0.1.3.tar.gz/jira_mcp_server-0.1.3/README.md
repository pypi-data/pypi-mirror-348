# Jira MCP Server (using FastMCP)

This MCP server provides tools for interacting with a Jira instance using username/password or session cookie authentication via the FastMCP framework. It allows LLMs (like Claude) to query, update, and manage Jira issues.

## Features

*   Connects to Jira using Basic Auth (username/password) or Session Cookie.
*   Provides MCP tools for common Jira operations:
    *   Fetching single or multiple issues.
    *   Creating and updating issues.
    *   Transitioning issue statuses.
    *   Listing available transitions.
    *   Adding comments.
    *   Downloading attachments.
    *   Listing project issue types.
*   Built with the modern and efficient FastMCP framework.

## Prerequisites

*   Python 3.10+
*   [uv](https://github.com/astral-sh/uv) (Recommended Python package installer and virtual environment manager)
*   Access to a Jira instance (Cloud or Server/Data Center).

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd jira-mcp-server
    ```

2.  **Configure Environment Variables:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   **Edit the `.env` file** with your Jira instance details:
        *   `JIRA_BASE_URL`: The full URL of your Jira instance (e.g., `https://yourcompany.atlassian.net` or `https://jira.yourdomain.com`).
        *   **Choose ONE authentication method:**
            *   **Method 1: Username/Password:** Set `JIRA_USERNAME` and `JIRA_PASSWORD`. (Note: For Jira Cloud, you might need an API Token instead of your password).
            *   **Method 2: Session Cookie:** Set `JIRA_SESSION_ID`. Get this value by logging into Jira in your browser, opening developer tools, going to Application/Storage -> Cookies, finding the cookie named `JSESSIONID` for your Jira domain, and copying its value. Session ID authentication takes precedence if set.
    *   **Important:** The `.env` file contains sensitive credentials and is included in `.gitignore` by default. **Do not commit your `.env` file to version control.**

3.  **Install Dependencies:**
    Create a virtual environment and install the required packages using `uv`:
    ```bash
    uv venv  # Create virtual environment in .venv
    uv sync # Install dependencies from pyproject.toml and uv.lock
    ```
    *   Activate the environment:
        *   macOS/Linux: `source .venv/bin/activate`
        *   Windows: `.venv\Scripts\activate`

## Project Structure

```
jira-mcp-server/
├── .env           # Your local environment variables (ignored by git)
├── .env.example   # Example environment file
├── .gitignore     # Files ignored by git
├── pyproject.toml # Project metadata and dependencies (uses Hatchling)
├── README.md      # This file
├── src/
│   └── jira_mcp/  # Main Python package for the server
│       ├── __init__.py
│       ├── __main__.py    # Entry point for `python -m jira_mcp`
│       ├── jira_client.py # Handles communication with the Jira API
│       ├── server.py      # Defines the FastMCP server and tools
│       └── settings.py    # Loads configuration using Pydantic Settings
└── uv.lock        # Lockfile for reproducible dependencies
```

*   **`src/jira_mcp/settings.py`**: Defines and loads configuration from the `.env` file.
*   **`src/jira_mcp/jira_client.py`**: Contains the `JiraClient` class that wraps the `jira-python` library, handling authentication and API calls asynchronously.
*   **`src/jira_mcp/server.py`**: Defines the `FastMCP` server instance (`mcp`) and registers all the Jira tools using the `@mcp.tool()` decorator. This is the main file referenced by `fastmcp` commands.
*   **`src/jira_mcp/__main__.py`**: Allows running the server directly using `python -m jira_mcp`.

## Running the Server

There are several ways to run the MCP server:

1.  **Directly using Python (via `__main__.py`):**
    This executes the `mcp.run()` command defined in `src/jira_mcp/__main__.py`, typically starting the server with the default `stdio` transport, which is expected by clients like Claude Desktop.
    ```bash
    # Make sure your virtual environment is activated
    python -m jira_mcp
    ```

2.  **Using `fastmcp run`:**
    This command directly loads and runs the `mcp` object from `server.py`, bypassing `__main__.py`. It also defaults to `stdio` but allows specifying other transports.
    ```bash
    # Run with default stdio transport
    fastmcp run src/jira_mcp/server.py:mcp

    # Run with SSE transport on port 8080 (example)
    fastmcp run src/jira_mcp/server.py:mcp --transport sse --port 8080
    ```

3.  **Using `fastmcp dev` (Recommended for Development):**
    This command runs the server and launches the MCP Inspector web UI, allowing you to interactively test tools and view protocol messages. It manages dependencies automatically based on `pyproject.toml`.
    ```bash
    fastmcp dev src/jira_mcp/server.py:mcp
    ```
    *   The Inspector UI will typically be available at `http://localhost:5173/`.
    *   The MCP server itself will be proxied by the Inspector, usually on a different port (check the command output).

## Building the Project

While typically run as a service or script, you can build distributable packages (wheel, sdist) if needed:

```bash
uv build
```

This will create the packages in the `dist/` directory. This is generally **not** required for simply running the server.

## Debugging

1.  **MCP Inspector (`fastmcp dev`):** The easiest way to debug interactions. You can see requests, responses, logs, and errors directly in the web UI.
2.  **FastMCP Logging:** FastMCP logs information to stderr by default. Increase verbosity by setting the log level when running:
    ```bash
    # Example with fastmcp run and SSE
    fastmcp run src/jira_mcp/server.py:mcp --transport sse --log-level DEBUG

    # Example with python -m (less direct control, relies on server default)
    # You might need to modify server.py's mcp.run() call to set log level
    # e.g., mcp.run(log_level="DEBUG") in __main__.py
    python -m jira_mcp
    ```
3.  **Standard Python Debugging:**
    *   When running directly with `python -m jira_mcp`, you can use standard Python debuggers like `pdb` or your IDE's debugger.
    *   Set breakpoints in `src/jira_mcp/server.py` or `src/jira_mcp/jira_client.py`.
    *   Example using `pdb`: Insert `import pdb; pdb.set_trace()` in the code where you want to pause.
    *   **Note:** Debugging might be more complex when using `fastmcp dev` or `fastmcp run` if they involve subprocess management that interferes with standard debugger attachment. Using `python -m` is often simplest for direct debugging.

## Configuration

Configuration is managed via environment variables or a `.env` file located in the project root. See `.env.example` for required variables.

*   `JIRA_BASE_URL` (Required)
*   `JIRA_USERNAME` / `JIRA_PASSWORD` (Required if `JIRA_SESSION_ID` is not set)
*   `JIRA_SESSION_ID` (Optional, takes precedence over username/password)

## Available Tools

The following tools are exposed by this MCP server:

*   **`jira_client_init`**: Initializes/verifies the Jira connection.
*   **`jira_get_issue`**: Retrieves details for a specific Jira issue by key.
*   **`jira_get_batch_issues`**: Retrieves details for multiple Jira issues by key.
*   **`jira_update_issue`**: Updates fields of an existing Jira issue. Can optionally add a comment.
*   **`jira_transition_issue`**: Changes the status of a Jira issue using a transition ID or name. Can include resolution, assignee, comment, and custom fields required by the transition screen.
*   **`jira_get_transitions`**: Lists the available status transitions for a specific Jira issue.
*   **`jira_download_attachments`**: Downloads all attachments for a specific Jira issue to a local directory.
*   **`jira_create_issue`**: Creates a new issue in a specified project.
*   **`jira_get_project_issue_types`**: Retrieves the available issue types (e.g., Bug, Task) for a specific Jira project.
*   **`jira_add_comment`**: Adds a comment to a specific Jira issue, optionally with visibility restrictions.
