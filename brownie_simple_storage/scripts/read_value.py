from brownie import SimpleStorage, accounts, config


def read_contract():
    """
    print(SimpleStorage[0]) # Actually Simple Storage is a array (deployments array) so we choose which deployment we use and thats it.

    """

    simple_storage = SimpleStorage[-1]  # -1 means latest

    """
    Normally to interact with contracts we should know its ABI and ADDRESS. Buttttt, BROWNIE knows it already. :)
    """

    readValue = simple_storage.retrieve()
    print(readValue)  # expected 53

    pass


def main():
    read_contract()
