"""Check the health of an EVM JSON-RPC endpoint."""

import argparse
import json
import os
import sys
import time
from typing import Any

from web3 import Web3


def check_rpc(rpc_url: str) -> dict[str, Any]:
    """Query an EVM JSON-RPC endpoint and return basic health information."""
    if not rpc_url.strip():
        raise ValueError("RPC URL cannot be empty")

    web3 = Web3(Web3.HTTPProvider(rpc_url.strip()))
    started = time.perf_counter()
    try:
        connected = web3.is_connected()
    except Exception as error:
        raise ConnectionError(f"RPC request failed: {error}") from error
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    if not connected:
        raise ConnectionError("Could not connect to RPC endpoint")

    try:
        chain_id = web3.eth.chain_id
        block_number = web3.eth.block_number
    except Exception as error:
        raise ConnectionError(f"Could not read network status: {error}") from error

    return {
        "status": "ok",
        "chain_id": chain_id,
        "block_number": block_number,
        "latency_ms": latency_ms,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check connectivity and basic status of an EVM JSON-RPC endpoint."
    )
    parser.add_argument(
        "--rpc",
        default=os.environ.get("RPC_URL"),
        help="EVM JSON-RPC endpoint (or set RPC_URL)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.rpc:
        parser.error("provide --rpc or set the RPC_URL environment variable")
    try:
        result = check_rpc(args.rpc)
    except (ValueError, ConnectionError) as error:
        print(json.dumps({"status": "error", "message": str(error)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
