# Arena PLM MCP Server

## Project Overview
MCP server that wraps Arena PLM's REST API, enabling Claude to search and retrieve part information via natural language.

## Architecture

```
Claude Code / Slackbot → MCP Server (stdio) → Arena PLM API
```

### Current Phase: Phase 1 (Native Search)
- Direct API wrapper exposing Arena's search as MCP tools
- Claude handles query interpretation, MCP handles API calls

### Future: Phase 2 (Semantic Search)
- Add vector DB (Chroma/pgvector) for embedding-based search
- Sync job to index parts from Arena
- New tool: `search_items_semantic(query: string)`

## Project Structure

```
arena-mcp-server/
├── src/
│   ├── server.py          # MCP server + tool definitions
│   ├── arena_client.py    # Arena API wrapper (auth, search)
│   └── config.py          # Credentials/env handling
├── Dockerfile
├── pyproject.toml
└── CLAUDE.md
```

## Arena API Details

- **Auth**: POST `/login` with email/password → returns `arena_session_id`
- **Search**: GET `/items` with query params (name, description, category.guid, etc.)
- **Wildcards**: Trailing `*` required for partial matches (e.g., `name=*bezel*`)
- **Pagination**: `limit` (max 400), `offset`
- **Response views**: `minimum`, `compact`, `full`

### Key Searchable Fields
- `name`, `description`, `number`
- `category.guid`, `owner.fullName`, `creator.fullName`
- `lifecyclePhase.guid`, `revisionNumber`
- Custom attributes via GUID: `?ATTR_GUID=*value*`

## MCP Tools

### `search_items`
Search Arena parts using native API filters.

**Parameters:**
- `name` (string, optional): Part name wildcard search
- `description` (string, optional): Description wildcard search
- `number` (string, optional): Part number search
- `category_guid` (string, optional): Category GUID filter
- `limit` (int, optional): Max results (default 20, max 400)

**Returns:** List of matching parts with number, name, revision, guid, url

### `get_item` (optional)
Fetch full details for a specific part.

**Parameters:**
- `guid` (string, required): Item GUID

## Running Locally

```bash
# Build
docker build -t arena-mcp-server .

# Run (stdio mode for MCP)
docker run -i --rm \
  -e ARENA_EMAIL=your-email \
  -e ARENA_PASSWORD=your-pass \
  -e ARENA_WORKSPACE_ID=your-workspace \
  arena-mcp-server
```

## Claude Code Config

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "arena-plm": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "ARENA_EMAIL", "-e", "ARENA_PASSWORD", "-e", "ARENA_WORKSPACE_ID", "arena-mcp-server"],
      "env": {
        "ARENA_EMAIL": "...",
        "ARENA_PASSWORD": "...",
        "ARENA_WORKSPACE_ID": "..."
      }
    }
  }
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ARENA_EMAIL` | Arena login email |
| `ARENA_PASSWORD` | Arena login password |
| `ARENA_WORKSPACE_ID` | Arena workspace ID |
| `ARENA_API_BASE` | API base URL (default: `https://api.arenasolutions.com/v1`) |

## Development Notes

- Server must use **stdio** transport for Docker MCP compatibility
- Arena sessions expire — implement token refresh or re-login on 401
- Wildcard searches: always wrap user input with `*` (e.g., `*bezel*`)
- URL-encode special characters in search params (`%`, `+`)

## Testing

```bash
# Test MCP connection
claude --mcp-debug

# In Claude Code
/mcp  # Should list arena-plm

# Test search
"Search for parts with 'bezel' in the name"
```

## Future Enhancements (Phase 2)

1. Add `vector_store.py` — Chroma/pgvector integration
2. Add `sync_job.py` — periodic Arena → vector DB sync
3. New tool: `search_items_semantic(query)` — embedding-based search
4. Keep `arena_client.py` decoupled for reuse