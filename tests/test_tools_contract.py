from dataclasses import dataclass

from crynux_mcp.server import handle_get_balance, handle_transfer_native


def test_handle_get_balance_shape(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    @dataclass(frozen=True)
    class FakeResult:
        network: str = "dymension"
        address: str = "0x1111111111111111111111111111111111111111"
        balance_wei: str = "100"
        balance_formatted: str = "0.0000000000000001"
        symbol: str = "CNX"
        chain_id: int = 1313161573

    class FakeClient:
        def __init__(self, _chain) -> None:
            pass

        def get_balance(self, address: str, unit: str | None = None):
            _ = (address, unit)
            return FakeResult()

    class FakeRegistry:
        def resolve(self, _network):
            return object()

    monkeypatch.setattr("crynux_mcp.server.EvmClient", FakeClient)
    monkeypatch.setattr("crynux_mcp.server.registry", FakeRegistry())

    payload = handle_get_balance(network="dymension", address="0x1111111111111111111111111111111111111111")
    assert payload["symbol"] == "CNX"
    assert payload["chain_id"] == 1313161573
    assert "text" in payload


def test_handle_transfer_sanitizes_private_key_error(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    class FakeClient:
        def __init__(self, _chain) -> None:
            pass

        def transfer_native(self, **_kwargs):
            raise ValueError("private key must be 32 bytes")

    class FakeRegistry:
        def resolve(self, _network):
            return object()

    monkeypatch.setattr("crynux_mcp.server.EvmClient", FakeClient)
    monkeypatch.setattr("crynux_mcp.server.registry", FakeRegistry())

    try:
        handle_transfer_native(
            network="dymension",
            private_key="0xabc",
            to="0x1111111111111111111111111111111111111111",
            amount="1",
        )
    except RuntimeError as exc:
        assert str(exc) == "INVALID_PRIVATE_KEY: private key is invalid."
    else:
        raise AssertionError("Expected RuntimeError")
