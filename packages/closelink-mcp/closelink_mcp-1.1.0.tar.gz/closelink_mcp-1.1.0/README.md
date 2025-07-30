## Publish new version

- Bump version

- Build

```bash
uv build
```

- Publish (See 1password for token)

```bash
 uv publish --username __token__ --password <PyPiApiToken>
```

## Usage

Mcp config:

```json
"closelink-mcp": {
    "command": "uvx",
    "args": [
        "closelink-mcp"
    ],
    "env": {
        "CLOSELINK_API_BASE_URL": "<ReplaceMe>",
        "CLOSELINK_API_KEY": "<ReplaceMe>"
    }
}
```
