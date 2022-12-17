from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import AdvancedCollectible, network
import json
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests


def main():

    filling()


def filling():
    account = get_account()
    # deploying
    advanced_collectible = AdvancedCollectible.deploy({"from": account})

    # creating web-page (opensea)
    tx1 = advanced_collectible.createCollectible(
        {"from": account}
    )  # made web-page-with-this
    tx1.wait(1)

    # we need metadata uri...
    make()


def make():
    collectible_metadata = metadata_template

    breed = "RIZE"
    image_path = f"./img/{breed.lower().replace('_','-')}.png"

    collectible_metadata["name"] = "EN-BUYUK-53 "
    collectible_metadata["description"] = f"EN BUYUK RIZE"
    collectible_metadata["image"] = upload_to_ipfs(image_path)  # URI

    advancedCollecible = AdvancedCollectible[-1]
    token_id = advancedCollecible.tokenCounter() - 1
    metadata_filename = f"./metadata/goerli/0-{breed}.json"

    with open(metadata_filename, "w") as file:
        json.dump(collectible_metadata, file)
    uri = upload_to_ipfs(metadata_filename)

    account = get_account()

    tx2 = AdvancedCollectible[-1].setTokenURI(
        AdvancedCollectible[-1].tokenCounter() - 1, uri, {"from": account}
    )
    tx2.wait(1)

    print(
        f"Welldone!, view on: {OPENSEA_URL.format(AdvancedCollectible[-1].address,AdvancedCollectible[-1].tokenCounter()-1)}"
    )


def upload_to_ipfs(file_path):  # generates URI.
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]  # Byte,Hash,Name,Size
        filename = file_path.split("/")[-1]
        image_uri = f"ipfs://{ipfs_hash}?filename={filename}"
        example = (
            "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
        )

        print(image_uri)

        return image_uri
