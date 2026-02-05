# Arena MCP Server

MCP server that wraps Arena PLM's REST API, enabling Claude to search and retrieve part information.

## Quick Start

```bash
docker compose up
```

## Development Commands

```bash
make dbuild           # Build Docker images
make drun             # Run containers in background
make dshell           # Open shell in running container
make dclean           # Stop and remove containers
make release VERSION=0.0.1  # Create and push version tag
```

## Releasing

To create a new release:

```bash
make release VERSION=0.0.1
```

This will:
1. Create a git tag `v0.0.1`
2. Push the tag to GitHub
3. Trigger GitHub Actions to build and push to `ghcr.io/carbonrobotics/arena-mcp-server:v0.0.1`

Monitor builds at: https://github.com/carbonrobotics/arena-mcp-server/actions

## Environment Variables

### Required
| Variable | Description |
|----------|-------------|
| `ARENA_EMAIL` | Arena PLM login email |
| `ARENA_PASSWORD` | Arena PLM login password |

### Google OAuth 2.0 (Production)
| Variable | Description |
|----------|-------------|
| `FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `FASTMCP_SERVER_AUTH_GOOGLE_BASE_URL` | Public URL for OAuth callbacks |

### Optional
| Variable | Description |
|----------|-------------|
| `ARENA_WORKSPACE_ID` | Workspace ID (uses default if not set) |
| `MCP_TRANSPORT` | Transport type: `http` or `sse` (default: `http`) |
| `MCP_HOST` | Host to bind (default: `0.0.0.0`) |
| `MCP_PORT` | Port to bind (default: `8080`) |
| `DISABLE_AUTH` | Set to `true` for local dev only (bypasses auth) |

## Available Tools

- `search_items` - Search parts by name, number, or description
- `get_item` - Get full details for an item by GUID
- `get_item_bom` - Get bill of materials for an assembly
- `get_item_where_used` - Find assemblies containing a part
- `get_item_revisions` - Get revision history
- `get_item_files` - Get associated files
- `get_item_sourcing` - Get supplier information
- `get_categories` - List item categories
