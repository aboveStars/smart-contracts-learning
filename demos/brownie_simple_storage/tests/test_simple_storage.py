from brownie import SimpleStorage, accounts


def test_deploy():
    # arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    startingValue = simple_storage.retrieve()
    expected = 0
    # Assert
    assert startingValue == expected


def test_updating_storage():
    # arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # act
    expected = 53
    simple_storage.store(expected, {"from": account})
    # assert
    assert simple_storage.retrieve() == expected
