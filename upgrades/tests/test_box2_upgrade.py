from scripts.helpful_scripts import get_account, upgrade, encode_function_data
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest


def test_proxy_upgrades():
    account = get_account()

    # deploying implemention 1
    box = Box.deploy({"from": account})

    # deploying admin proxy
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # hook box with proxy

    encoded_data = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_data,
        {"from": account, "gas_limit": 10000000},
    )

    proxy_box = Contract.from_abi(
        "Box", proxy.address, Box.abi
    )  # to use contract where on proxy
    assert proxy_box.retrieve() == 0
    proxy_box.store(53, {"from": account})

    box2 = BoxV2.deploy({"from": account})

    upgrade_tx = upgrade(account, proxy, box2.address, proxy_admin)
    upgrade_tx.wait(1)

    box_upgraded = Contract.from_abi("BoxV2", proxy, BoxV2.abi)
    assert box_upgraded.retrieve() == 53
    box_upgraded.incremant({"from": account})
    assert box_upgraded.retrieve() == 54
