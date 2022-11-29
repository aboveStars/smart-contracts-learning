from brownie import accounts, network, exceptions
from scripts.deploy import deploy_fund_me, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.helpful_scripts import get_account
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entranceFee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account) == entranceFee

    tx2 = fund_me.withdraw({"from": get_account()})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only For Local Testing")

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
