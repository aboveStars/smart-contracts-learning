from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import AdvancedCollectible, network
import json
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests


def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()

    # deploying
    advanced_collectible = AdvancedCollectible.deploy({"from": account})

    # First step of sending NFT to OpenSea...
    # This is for cretaing blank OpenSea page.
    tx1 = advanced_collectible.createCollectible(
        {"from": account}
    )  # made web-page-with-this
    tx1.wait(1)

    # we need metadata uri...
    uploadFiles_GenerateURIs_SendURIs()


def uploadFiles_GenerateURIs_SendURIs():
    # Giving Name and directory of image for NFT.
    breed = "RIZE"
    image_path = f"./img/{breed.lower().replace('_','-')}.png"

    # Creating MetaData file
    collectible_metadata = metadata_template

    collectible_metadata["name"] = "EN-BUYUK-53 "
    collectible_metadata["description"] = f"EN BUYUK RIZE"
    collectible_metadata["image"] = uploadToIPFS_and_generateURI(
        image_path
    )  # Put the IMAGE URI to metadata

    # Giving metaData file's location or directory
    metadata_filename = f"./metadata/goerli/0-{breed}.json"

    # Making JSON file from metadata
    with open(metadata_filename, "w") as file:
        json.dump(collectible_metadata, file)

    # Sending metadata to IPFS and generating URI.
    # We use this URI (metadata URI) for sending to OpenSea.
    uri = uploadToIPFS_and_generateURI(metadata_filename)

    # Sending to the OpenSea. (actually we are sending just metadataURI which also contains imageURI)
    account = get_account()
    tx2 = AdvancedCollectible[-1].setTokenURI(
        AdvancedCollectible[-1].tokenCounter() - 1, uri, {"from": account}
    )
    tx2.wait(1)

    # Result
    print(
        f"Welldone!, view on: {OPENSEA_URL.format(AdvancedCollectible[-1].address,AdvancedCollectible[-1].tokenCounter()-1)}"
    )


def uploadToIPFS_and_generateURI(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()

        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"

        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()[
            "Hash"
        ]  # Byte,Hash,Name,Size is come. We take whatever we want. # For URI we need HASH.

        filename = file_path.split("/")[-1]

        image_uri = (
            f"ipfs://{ipfs_hash}?filename={filename}"  # Combining all stuff for URI.
        )
        example_uri = (
            "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
        )

        # For IPFS links...
        print(image_uri)

        return image_uri
