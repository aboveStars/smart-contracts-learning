import requests
from pathlib import Path


def test1():
    animal_name = "ST_BERNARD"
    image_path = f"./img/{animal_name.lower().replace('_','-')}.png"
    print(upload_to_ipfs(image_path))


def upload_to_ipfs(file_path):
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


test1()
