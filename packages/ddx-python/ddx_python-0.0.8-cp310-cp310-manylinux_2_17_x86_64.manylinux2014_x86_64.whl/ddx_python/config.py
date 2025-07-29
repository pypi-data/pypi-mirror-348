import os

from ddx_python._ddx_python import common

# FIXME: might need to change these environment variables to `DDX_CONTRACT_DEPLOYMENT` for better convention


def load_mainnet():
    os.environ["CONTRACT_DEPLOYMENT"] = "derivadex"
    common.reinit_operator_context()


def load_testnet():
    os.environ["CONTRACT_DEPLOYMENT"] = "testnet"
    common.reinit_operator_context()
