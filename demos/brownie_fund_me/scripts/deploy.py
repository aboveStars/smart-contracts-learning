from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    # pass the address to CONSTRUCTER

    # if we are on real use address.

    """
    Aggreagtor'de Ne Yaptık ? 

    Normalde Aggregator online bir contract. Biz online-chain de iş yaparken Aggreagator(address) verdiğimizde
    internetten gerekli contractı buluyordu.

    Ama localde çalışınca bizim sanki ona bir address verdikte o da buldu gibi hareket etmesini sağlamamız lazım. Bunun için de
    aynı görevi (tabi ki sahte, meseka önceden ayarlı ETH ücreti gibi) yapan ve addreesini bildiğimiz bir contract oluşturup bu adresi
    Aggregator(ID) id kısmına basıyoruz.

    
    """

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        priceFeedAddress = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    else:
        deploy_mocks()
        priceFeedAddress = MockV3Aggregator[-1]

    fund_me = FundMe.deploy(
        priceFeedAddress,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Contract deployed to {fund_me}")
    return fund_me


def main():
    deploy_fund_me()
