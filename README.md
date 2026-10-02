# EVM RPC Healthcheck

A small Python CLI that checks whether an EVM JSON-RPC endpoint responds and reports its chain ID, latest block number, and connection-check latency.

## Requirements

- Python 3.10 or newer
- An EVM-compatible JSON-RPC endpoint

## Install

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python src/healthcheck.py --rpc "https://YOUR_RPC_ENDPOINT"
```

Or set `RPC_URL` in your shell:

```powershell
$env:RPC_URL = "https://YOUR_RPC_ENDPOINT"
python src/healthcheck.py
```

```bash
export RPC_URL="https://YOUR_RPC_ENDPOINT"
python src/healthcheck.py
```

Successful output looks like:

```json
{
  "status": "ok",
  "chain_id": 1,
  "block_number": 123456,
  "latency_ms": 42.18
}
```

Latency measures the JSON-RPC connectivity check. Keep private or paid RPC URLs out of public commits. `.env.example` is a template and is not loaded automatically.

## Tests

Tests use Python's standard `unittest` framework and mock Web3. They need no internet access or live RPC:

```bash
python -m unittest discover -s tests -v
```

## GitHub Actions

Pushes and pull requests run unit tests on Python 3.10, 3.11, and 3.12. No RPC secret is required.

## License

MIT. See [LICENSE](LICENSE).
