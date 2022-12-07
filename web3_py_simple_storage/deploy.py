from solcx import compile_standard  # , install_solc

# install_solc("0.6.0") If we need install older versions...

import json

from web3 import Web3

import os

from dotenv import load_dotenv

load_dotenv()  # this pushes automatically our .env file to terminal and NICE!!!


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# Compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
)

# To read easily... (just for this)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get-byte-code
byteCode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get-abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# LOCAL CONNECTION
"""
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337  # THIS IS NOT GANACHE NETWORK ID, THIS IS CONSTANT
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

# private_key = "0x4701xxxxcxxxxxx3xxx18xxxx0xcc5eda183b0axxxxxxxxxxxx"  # 0x added to start
## HARD CODE NOT RECOMENDED WE USE OS_ENV

private_key = os.getenv("PRIVATE_KEY")

"""
# REAL CONNECTION (GOERLI...)

w3 = Web3(
    Web3.HTTPProvider("https://goerli.infura.io/v3/3ad97cd8be5f47f29ae1a52787fbac71")
)
chain_id = 5  # from chainList
my_address = "0x54D2C9AB8C19CCA0bA9A5F161B65AE7032179E6B"
private_key = os.getenv("PRIVATE_KEY_GOERLI")

# create contract with python

SimpleStorage = w3.eth.contract(abi=abi, bytecode=byteCode)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

"""
1- Build Transaction
2- Sign Transaction
3- Send Transaction

"""


# Build
transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

# SIGN
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# SEND
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("DEPLOYING CONTRACT......")
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("CONTRACT DEPLOYED !!!")

# INTERACTIN WITH CONTRACT
"""
WORKING WITH CONTRACT WE NEED:
1) CONTRACT ADDRESS
2) CONTRACT ABI

"""
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call -> simulate making the call and getting a return value (BLUE) (SIMULATION)
# transact -> actually making state change (orange) (REAL)

# INITIAL FAVORITE NUMBER (call)
print(
    f" Calling Favorite Number First Time:  {simple_storage.functions.retrieve().call()}"
)  ## THIS IS OKAY BECAUSE retrieve ALREADY View Function >> returns 0
print(
    f" CALLING store function: {simple_storage.functions.store(384).call()}"
)  ## BUT store Is transact Function (orange) so it can be CALLed. But It will not affect the chain... IT IS A SIMULATION >> returns 384
print(
    f" Calling Favorite Number Second Time: {simple_storage.functions.retrieve().call()}"
)  ## as we see we didn't make any changes above because we just CALLed it. >> returns 0

# SET FAVORITE NUMBER (TRANSACT)

# Build
store_transaction = simple_storage.functions.store(53).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
        + 1,  # because of we deployed contract with "nonce" already and they can not be same so we added 1 to nonce
        "gasPrice": w3.eth.gasPrice,
    }
)

# Sign
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# Send
sendStoreTx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
print("CONTRACT UPDATING.........")
tx_receipt = w3.eth.wait_for_transaction_receipt(sendStoreTx)
print("CONTRACT UPDATED")
print(
    f"Caling Favorite Number After State Changing:  {simple_storage.functions.retrieve().call()}"
)
