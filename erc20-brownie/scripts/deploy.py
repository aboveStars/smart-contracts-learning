from brownie import RizeToken, accounts
from scripts.helpful_scripts import get_account
from web3 import Web3

initialSupply = Web3.toWei(1000, "ether")


def deploy():
    account = get_account()
    rizeToken = RizeToken.deploy(initialSupply, {"from": account})
    print(rizeToken.name())


def main():
    deploy()
