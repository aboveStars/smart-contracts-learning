from brownie import AdvancedCollectible, accounts
from scripts.helpful_scripts import get_account

def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    creation_tx = advanced_collectible.createCollectible({"from":account})
    creation_tx.wait(1)
    print("Collectible Created!")
    