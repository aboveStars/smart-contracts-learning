from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path


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
        print(metadata_filename)
        if Path(metadata_filename).exists():
            print(
                f"{metadata_filename} is already exists. Please delete it to overwrite"
            )
        else:
            print(f"Creating metadata file: {metadata_filename}")
