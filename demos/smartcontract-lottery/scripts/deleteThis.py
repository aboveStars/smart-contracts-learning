from brownie import Lottery, accounts, network, config


def test_getEntranceFee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )

    print(lottery.getEnteranceFee())


def main():
    test_getEntranceFee()
