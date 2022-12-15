from brownie import network, accounts, config

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]

OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"
BREED_MAPPING = {0:"PUG",1:"SHIBA_INU",2:"ST_BERNARD"}

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

