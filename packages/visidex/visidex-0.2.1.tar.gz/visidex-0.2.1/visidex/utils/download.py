import os
import urllib
from typing import Optional
import torch
import zipfile
import requests


def download_file(url: str, local_path: str) -> None:
    """
    Download an artifact file from a given URL if it doesn't already exist locally.

    Args:
        url (str): URL to download the artifact from.
        local_path (str): Local path to save the artifact file.
    """
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not os.path.exists(local_path):
        print(f"Downloading artifact from {url} ...")
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print(f"artifact downloaded and saved to {local_path}")
    else:
        print(f"artifact already exists at {local_path}. Skipping download.")


def load_model(model: torch.nn.Module, model_path: str, map_location='cpu') -> Optional[torch.nn.Module]:
    if model is None:
        raise ValueError("A model instance must be provided.")
    print(f"Loading model weights from {model_path} ...")
    state_dict = torch.load(model_path, map_location=map_location, weights_only=True)
    model.load_state_dict(state_dict)
    print("Model loaded successfully.")
    return model

def extract_zip(zip_path: str, extract_to: str = None):
    """
    Extracts a .zip file to a specified directory.

    Args:
        zip_path (str): Path to the .zip file.
        extract_to (str, optional): Directory to extract contents to.
                                    Defaults to same directory as zip file.
    """
    if extract_to is None:
        extract_to = os.path.splitext(zip_path)[0]  # same name, no .zip

    os.makedirs(extract_to, exist_ok=True)

    print(f"Extracting {zip_path} to {extract_to} ...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete.")

# if __name__ == '__main__':
#     url ="https://github.com/binarycode11/visidex/raw/refs/heads/main/data/dataset/fibers.zip"
#     local_path ="./tests/fibers.zip"
#     download_file(url,local_path)
#     extract_zip(local_path,"./tests/")
#
#     url ="https://github.com/binarycode11/visidex/raw/refs/heads/main/data/dataset/wood_dataset.zip"
#     local_path ="./tests/wood_dataset.zip"
#     download_file(url,local_path)
#     extract_zip(local_path,"./tests/")