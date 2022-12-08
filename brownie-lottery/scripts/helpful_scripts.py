from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    Contract,
    VRF_CoordinatorV2Mock,
    LinkToken,
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = {"development", "ganache-local"}
FORKED_LOCAL_ENVIRONMENTS = {"mainnet-fork-dev"}


def get_account(index=None, id=None):

    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRF_CoordinatorV2Mock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """
    This Function will grab the contract adress from Brownie Config if defined.
    Otherwise, iw will deploy a mock version.
    Returns a contract.

        Args:
            Contract Name (String)
        Returns:
            bronwnie.network.contract.ProjectContract (MostRecent)

    """
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # abi
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


DECIMALS = 8
STARTINGPRICE = 200000000000


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(
        {"from": account}, decimals=DECIMALS, initial_value=STARTINGPRICE
    )
    link_token = LinkToken.deploy({"from": account})
    VRF_CoordinatorV2Mock.deploy({"from": account}, link_token.address)
    print("Deployed Mocks !")
