from brownie import network, accounts, config
import eth_utils

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]

OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


# initalizer: box.store, 1
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implemention_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implemention_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implemention_address, {"from": account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implemention_address, encoded_function_call, {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(new_implemention_address, {"from": account})
    return transaction
