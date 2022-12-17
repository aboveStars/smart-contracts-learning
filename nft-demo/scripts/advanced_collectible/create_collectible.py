from brownie import AdvancedCollectible, accounts
from scripts.helpful_scripts import get_account

def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    
    # creating web-page (opensea)
    tx1 = advanced_collectible.createCollectible({"from":account}) # made web-page-with-this
    tx1.wait(1)
    