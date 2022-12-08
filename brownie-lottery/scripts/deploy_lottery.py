from brownie import Lottery, config, network
from scripts.helpful_scripts import get_account, get_contract


def main():
    deployLottery()


def deployLottery():
    account = get_account(id="fcc-demo")
    lottery = Lottery.deploy(
        {"from": account},
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print("Deployed Lottery !")
