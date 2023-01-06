from brownie import Lottery, accounts, config
from web3 import Web3


def main():
    deploy_lottery()


def deploy_lottery():
    signer = accounts.add(config["wallets"]["from_key"])

    _interval = 100
    _fee = Web3.toWei(0.1, "ether")
    _vrf = "0x2Ca8E0C643bDe4C2E08ab1fA0da3401AdAD7734D"
    _gasLane = "0x79d3d8832d904592c0bf9818b621522c988bb8b0c05cdc3b15aea1b6e8db0c15"
    _subId = 8343
    _callbackGasLimit = 250000

    lottery = Lottery.deploy(
        _interval,
        _fee,
        _vrf,
        _gasLane,
        _subId,
        _callbackGasLimit,
        {"from": signer},
        publish_source=True,
    )
