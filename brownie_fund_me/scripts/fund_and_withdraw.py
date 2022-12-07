from brownie import accounts, FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"Current entry fee is {entrance_fee}")
    print("Funding Started")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
