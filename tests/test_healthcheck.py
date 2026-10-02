import unittest
from unittest.mock import MagicMock, patch

from src.healthcheck import check_rpc


class CheckRpcTests(unittest.TestCase):
    @patch("src.healthcheck.time.perf_counter", side_effect=[1.0, 1.025])
    @patch("src.healthcheck.Web3")
    def test_returns_chain_block_and_latency(self, web3_class, _clock):
        web3 = MagicMock()
        web3.is_connected.return_value = True
        web3.eth.chain_id = 8453
        web3.eth.block_number = 12_345
        web3_class.return_value = web3

        result = check_rpc(" https://rpc.example.invalid ")

        self.assertEqual(result, {
            "status": "ok",
            "chain_id": 8453,
            "block_number": 12_345,
            "latency_ms": 25.0,
        })
        web3_class.HTTPProvider.assert_called_once_with("https://rpc.example.invalid")

    @patch("src.healthcheck.Web3")
    def test_reports_unreachable_endpoint(self, web3_class):
        web3 = MagicMock()
        web3.is_connected.return_value = False
        web3_class.return_value = web3

        with self.assertRaisesRegex(ConnectionError, "Could not connect"):
            check_rpc("https://rpc.example.invalid")

    @patch("src.healthcheck.Web3")
    def test_rejects_empty_url(self, web3_class):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            check_rpc("   ")
        web3_class.assert_not_called()

    @patch("src.healthcheck.Web3")
    def test_reports_network_read_error(self, web3_class):
        web3 = MagicMock()
        web3.is_connected.return_value = True
        type(web3.eth).chain_id = property(lambda _self: (_ for _ in ()).throw(RuntimeError("bad response")))
        web3_class.return_value = web3

        with self.assertRaisesRegex(ConnectionError, "Could not read network status"):
            check_rpc("https://rpc.example.invalid")


if __name__ == "__main__":
    unittest.main()
