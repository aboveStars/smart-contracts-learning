from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIDtoBreed(token_id))
        # ex. 7 (as tokenID) --> 2 (in that token ID, it has ST_BERNARD BUT returns its index...) --> ST_BERNARD (from dict)
        metadata_filename = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )

        if Path(metadata_filename).exists():
            print(
                f"{metadata_filename} is already exists. Please delete it to overwrite"
            )
        else:
            print(f"Creating metadata file: {metadata_filename}")

            collectible_metadata = metadata_template
            image_path = f"./img/{breed.lower().replace('_','-')}.png"

            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            collectible_metadata["image"] = upload_to_ipfs(image_path)  # URI

            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)

            print(f"Our JSON-URI = {upload_to_ipfs(metadata_filename)}") ## yes just this. (because funciton uploads...)

            """
            We should send img and metadata ,that contains img uri also, seperatly.
            """
            return 


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
        return image_uri
