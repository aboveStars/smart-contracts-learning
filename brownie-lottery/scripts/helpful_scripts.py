from brownie import (
    accounts,
    config,
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = {"development", "ganache-local"}
FORKED_LOCAL_ENVIRONMENTS = {"mainnet-fork-dev"}


def get_account(index=None, id=None):
    return accounts.add(config["wallets"]["from_key"])
