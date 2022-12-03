from brownie import Lottery
from helpful_scripts import get_account


def main():
    deployLottery()


def deployLottery():
    account = get_account()
    lottery = Lottery.deploy()
