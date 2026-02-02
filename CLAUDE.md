# Arena MCP Server

MCP server wrapping Arena PLM's REST API.

## Commands

```bash
docker compose up          # Run server
docker compose up --build  # Rebuild and run
```

## Structure

- `server.py` - MCP tools and Scalekit OAuth 2.1 authentication
- `arena_client.py` - Arena REST client (httpx, session-based auth)

## Environment

Required in `.env`:
- `ARENA_EMAIL`, `ARENA_PASSWORD` - Arena PLM credentials

Scalekit OAuth 2.1 (required for production):
- `SCALEKIT_ENVIRONMENT_URL` - Scalekit environment URL (e.g., `https://your-env.scalekit.com`)
- `SCALEKIT_RESOURCE_ID` - Resource ID from Scalekit dashboard (e.g., `res_...`)
- `MCP_URL` - Public URL where this MCP server is accessible (for OAuth callbacks)

Optional:
- `ARENA_WORKSPACE_ID` (uses default workspace if not set)
- `MCP_TRANSPORT` (http or sse, defaults to http)
- `MCP_HOST` (defaults to 0.0.0.0)
- `MCP_PORT` (defaults to 8080)
- `DISABLE_AUTH=true` (disables auth for local development - use only locally)

## Authentication

The server uses **Scalekit OAuth 2.1** for MCP client authentication (via `fastmcp.server.auth.providers.scalekit.ScalekitProvider`).

**Local development:**
- Set `DISABLE_AUTH=true` to bypass authentication entirely
- This should NEVER be used in production

## Gotchas

- Arena API requires `*wildcards*` for partial matches - `arena_client.py` adds them automatically
- No session refresh on expiry - will error, needs re-auth
- No rate limit retry logic
- Arena auth is lazy (first tool call), not at startup
- OAuth requires publicly accessible URL (use ngrok/cloudflare tunnel for local dev)
