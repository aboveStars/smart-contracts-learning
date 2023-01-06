from brownie import Lottery, accounts, config
from web3 import Web3


def main():
    enterToLottery()


def enterToLottery():
    lottery = Lottery[-1]

    fee = Web3.toWei(0.1, "ether")

    signer = accounts.add(config["wallets"]["from_key"])

    lottery.enterToLottery({"value": fee, "from": signer})

