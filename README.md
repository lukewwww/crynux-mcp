# crynux-mcp

Python MCP server for Crynux EVM L2 blockchain operations.

## Scope

- Native CNX balance query on Crynux EVM networks
- Native CNX transfer with locally provided private key
- Relay API integration is not implemented yet

## Spec and transport

- MCP protocol target: `2025-11-25`
- Runtime transport: `stdio` (local process, no HTTP server required)

## Tools

### `get_balance`

Inputs:
- `network`: optional (`dymension` or `near`). Defaults to configured default network.
- `address`: EVM address
- `unit`: optional, `wei` or `ether` (default: `ether`)

Output fields:
- `network`
- `address`
- `balance_wei`
- `balance_formatted`
- `symbol` (`CNX`)
- `chain_id`

### `transfer_native`

Inputs:
- `network`: optional (`dymension` or `near`). Defaults to configured default network.
- `private_key`: EVM private key (passed per tool call)
- `to`: recipient EVM address
- `amount`: numeric string
- `unit`: optional, `wei` or `ether` (default: `ether`)
- `gas_price_wei`: optional override
- `gas_limit`: optional override

Output fields:
- `network`
- `from_address`
- `to`
- `value_wei`
- `tx_hash`
- `chain_id`

## Security notes

- The server never intentionally logs raw private keys.
- Private key input is only used in-memory for the current call.
- Tool-call private keys can still appear in host-side chat/tool history depending on client behavior.
- Use dedicated low-risk wallets for AI operations, not treasury wallets.

## Get Started

### Step 1) Prerequisites

- Install Python 3.11 or newer.
- Open a terminal in this repository root: `crynux-mcp`.

### Step 2) Install the package

Install from PyPI (recommended):

```bash
python -m pip install crynux-mcp
```

If you are developing this repository, install from source in editable mode:

```bash
python -m pip install -e ".[dev]"
```

### Step 3) Choose your AI client and add MCP config

You only need one client config (Cursor, VS Code, or Claude Desktop).

#### Cursor

Create or edit `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "crynux-mcp": {
      "command": "python",
      "args": ["-m", "crynux_mcp"]
    }
  }
}
```

#### VS Code

Create or edit `.vscode/mcp.json` in your project (or your user `mcp.json`):

```json
{
  "servers": {
    "crynuxMcp": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "crynux_mcp"]
    }
  }
}
```

#### Claude Desktop

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "crynux-mcp": {
      "command": "python",
      "args": ["-m", "crynux_mcp"]
    }
  }
}
```

### Step 4) Restart your AI client

After saving MCP config, fully restart the client so it reloads servers.

### Step 5) Verify the server is loaded

In your AI client, check MCP tool list and confirm these tools appear:

- `get_balance`
- `transfer_native`

### Step 6) First tool calls

Example: query balance

- `network`: `dymension`
- `address`: your EVM address
- `unit`: `ether`

Example: send native CNX

- `network`: `dymension`
- `private_key`: sender private key
- `to`: recipient EVM address
- `amount`: for example `0.1`
- `unit`: `ether`

### Step 7) Optional local manual run

You can start the MCP server process directly for debugging:

```bash
python -m crynux_mcp
```

## Release

Maintainer release instructions are in [`RELEASE.md`](./RELEASE.md).

## Network configuration

Chain metadata is stored in:

- `src/crynux_mcp/config/chains.json`

Update this file to change RPC URLs, chain IDs, or contract addresses.

## Tests

```bash
pytest
```
