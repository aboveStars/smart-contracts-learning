from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import AdvancedCollecible

def deploy_and_create():
    account = get_account()

    advanced_collectible = AdvancedCollecible.deploy({"from": account})

    creating_tx = advanced_collectible.createCollectible({"from":account})
    creating_tx.wait(1)
    print("New nft has been created")

    


def main():
    deploy_and_create()
