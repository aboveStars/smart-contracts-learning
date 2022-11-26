from brownie import accounts, config, SimpleStorage

# import os


def deploy_simple_storage():
    account = accounts[0]

    simple_storage = SimpleStorage.deploy(
        {"from": account}
    )  # transact or call... Brownie king understand...Also this line makes: Build, sign, and send! But we should put address if we make transaction

    stored_value = (
        simple_storage.retrieve()
    )  # we dont need add account becasue we dont make a transaction
    print(f"First favoriteNumber: {stored_value}")

    transaction = simple_storage.store(53, {"from": account})
    transaction.wait(1)

    updatedFavoriteNumber = simple_storage.retrieve()
    print(updatedFavoriteNumber)

    # account = accounts.load("fcc-demo")
    # print(account)
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


def main():
    deploy_simple_storage()
