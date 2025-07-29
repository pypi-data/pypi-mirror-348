import unittest

from ddx_python import load_mainnet, load_testnet


class DdxCommonTests(unittest.TestCase):
    def test_app_context(self):
        from ddx_python.common import TokenSymbol, get_operator_context

        load_mainnet()
        mainnet_usdc = TokenSymbol.USDC.address()
        load_testnet()
        testnet_usdc = TokenSymbol.USDC.address()

        self.assertNotEqual(mainnet_usdc, testnet_usdc)


if __name__ == "__main__":
    unittest.main()
