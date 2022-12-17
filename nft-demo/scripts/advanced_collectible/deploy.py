from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import AdvancedCollecible


def main():
    deploying()


def deploying():
    account = get_account()
    # deploying
    advanced_collectible = AdvancedCollecible.deploy({"from": account})
