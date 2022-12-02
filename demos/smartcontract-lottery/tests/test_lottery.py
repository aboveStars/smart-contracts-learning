# 0.038 expected
# 38 000 000 000 000 000 in other way
from brownie import Lottery, accounts, network, config
from web3 import Web3


def test_getEntranceFee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )

    print(lottery.getEnteranceFee())

    assert lottery.getEnteranceFee() > Web3.toWei(0.030, "ether")
    assert lottery.getEnteranceFee() < Web3.toWei(0.040, "ether")
