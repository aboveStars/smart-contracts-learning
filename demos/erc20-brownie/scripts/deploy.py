from brownie import RizeToken, accounts
from scripts.helpful_scripts import get_account
from web3 import Web3

initialSupply = Web3.toWei(1000, "ether")


def deploy():
    account = get_account()
    RizeToken.deploy(530000000000000000, {"from": account})
    balanceViewer()


def balanceViewer():
    print(RizeToken[-1].balanceOf("0x54D2C9AB8C19CCA0bA9A5F161B65AE7032179E6B"))


def main():
    deploy()
