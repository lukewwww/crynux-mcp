from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from mcp.server.fastmcp import FastMCP

from crynux_mcp.blockchain.evm_client import EvmClient
from crynux_mcp.config.loader import load_chain_registry
from crynux_mcp.security.redaction import redact_secrets, sanitize_error_message

mcp = FastMCP("crynux-mcp")
registry = load_chain_registry()


def _to_response_payload(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        payload = asdict(value)
    elif isinstance(value, dict):
        payload = value
    else:
        payload = {"value": value}
    payload["text"] = json.dumps(payload, ensure_ascii=True)
    return payload


def _execution_error(exc: Exception, args: dict[str, Any] | None = None) -> RuntimeError:
    _ = redact_secrets(args or {})
    message = sanitize_error_message(str(exc))
    return RuntimeError(message)


def handle_get_balance(network: str | None, address: str, unit: str | None = None) -> dict[str, Any]:
    try:
        chain = registry.resolve(network)
        client = EvmClient(chain)
        result = client.get_balance(address=address, unit=unit)
        return _to_response_payload(result)
    except Exception as exc:  # noqa: BLE001
        raise _execution_error(exc, {"network": network, "address": address, "unit": unit}) from exc


def handle_transfer_native(
    network: str | None,
    private_key: str,
    to: str,
    amount: str,
    unit: str | None = "ether",
    gas_price_wei: int | None = None,
    gas_limit: int | None = None,
) -> dict[str, Any]:
    try:
        chain = registry.resolve(network)
        client = EvmClient(chain)
        result = client.transfer_native(
            private_key=private_key,
            to=to,
            amount=amount,
            unit=unit,
            gas_price_wei=gas_price_wei,
            gas_limit=gas_limit,
        )
        return _to_response_payload(result)
    except Exception as exc:  # noqa: BLE001
        raise _execution_error(
            exc,
            {
                "network": network,
                "private_key": private_key,
                "to": to,
                "amount": amount,
                "unit": unit,
                "gas_price_wei": gas_price_wei,
                "gas_limit": gas_limit,
            },
        ) from exc


@mcp.tool()
def get_balance(network: str | None, address: str, unit: str | None = None) -> dict[str, Any]:
    """Get native CNX balance on a selected Crynux EVM network."""
    return handle_get_balance(network=network, address=address, unit=unit)


@mcp.tool()
def transfer_native(
    network: str | None,
    private_key: str,
    to: str,
    amount: str,
    unit: str | None = "ether",
    gas_price_wei: int | None = None,
    gas_limit: int | None = None,
) -> dict[str, Any]:
    """Transfer native CNX by signing a transaction with the provided private key."""
    return handle_transfer_native(
        network=network,
        private_key=private_key,
        to=to,
        amount=amount,
        unit=unit,
        gas_price_wei=gas_price_wei,
        gas_limit=gas_limit,
    )


def run() -> None:
    mcp.run(transport="stdio")
