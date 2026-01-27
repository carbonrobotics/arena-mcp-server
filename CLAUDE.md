# Arena MCP Server

MCP server wrapping Arena PLM's REST API.

## Commands

```bash
docker compose up          # Run server
docker compose up --build  # Rebuild and run
```

## Structure

- `server.py` - MCP tools and auth (`APIKeyVerifier` subclasses `TokenVerifier`)
- `arena_client.py` - Arena REST client (httpx, session-based auth)

## Environment

Required in `.env`:
- `ARENA_EMAIL`, `ARENA_PASSWORD`

Authentication:
- `MCP_API_KEY` (min 32 chars, server denies all access if unset)
- `DISABLE_AUTH=true` (disables auth for local development - use only locally)

Optional:
- `ARENA_WORKSPACE_ID` (uses default workspace if not set)
- `MCP_TRANSPORT` (http or sse, defaults to http)
- `MCP_HOST` (defaults to 0.0.0.0)
- `MCP_PORT` (defaults to 8080)

## Gotchas

- Arena API requires `*wildcards*` for partial matches - `arena_client.py` adds them automatically
- No session refresh on expiry - will error, needs re-auth
- No rate limit retry logic
- Auth is lazy (first tool call), not at startup
