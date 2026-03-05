# Tool Reference

This document contains detailed input and output fields for each MCP tool.

## `get_balance`

Inputs:
- `network`: optional (`dymension` or `near`). Defaults to configured default network.
- `address`: EVM address.
- `unit`: optional, `wei` or `ether` (default: `ether`).

Output fields:
- `network`
- `address`
- `balance_wei`
- `balance_formatted`
- `symbol` (`CNX`)
- `chain_id`

## `transfer_native`

Inputs:
- `network`: optional (`dymension` or `near`). Defaults to configured default network.
- `key_name`: optional signer key name. Uses default local key if omitted.
- `to`: recipient EVM address.
- `amount`: numeric string.
- `unit`: optional, `wei` or `ether` (default: `ether`).
- `gas_price_wei`: optional override.
- `gas_limit`: optional override.

Output fields:
- `network`
- `from_address`
- `to`
- `value_wei`
- `tx_hash`
- `chain_id`

## `get_beneficial_address`

Inputs:
- `network`: optional (`dymension` or `near`). Defaults to configured default network.
- `node_address`: operational EVM address to query.

Output fields:
- `network`
- `node_address`
- `beneficial_address`
- `is_set`: `true` when beneficial address is not zero address.
- `contract_address`
- `chain_id`

## `set_beneficial_address`

Inputs:
- `network`: optional (`dymension` or `near`). Defaults to configured default network.
- `key_name`: optional signer key name. Uses default local key if omitted.
- `beneficial_address`: target beneficial EVM address.
- `gas_price_wei`: optional override.
- `gas_limit`: optional override.

Output fields:
- `network`
- `node_address`: signer address that submits the transaction.
- `beneficial_address`
- `tx_hash`
- `contract_address`
- `chain_id`

## `create_key`

Inputs:
- `name`: signer key name.

Output fields:
- `name`
- `address`

## `list_keys`

Inputs:
- No input fields.

Output fields:
- `keys`: array of key records.
- `count`: number of keys.

Each key record contains:
- `name`
- `address`
- `is_default`

## `delete_key`

Inputs:
- `name`: signer key name to delete.

Output fields:
- `name`
- `deleted`

## `set_default_key`

Inputs:
- `name`: signer key name to set as default.

Output fields:
- `name`
- `address`
- `is_default`

## `export_key`

Inputs:
- `name`: signer key name to export.
- `filename`: destination file path.

Output fields:
- `name`
- `filename`
- `written`
