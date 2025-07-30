import os
import urllib
from typing import Optional

import torch

import os
import torch
import requests


def download_model(url: str, local_path: str) -> None:
    """
    Download a model file from a given URL if it doesn't already exist locally.

    Args:
        url (str): URL to download the model from.
        local_path (str): Local path to save the model file.
    """
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    if not os.path.exists(local_path):
        print(f"Downloading model from {url} ...")
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print(f"Model downloaded and saved to {local_path}")
    else:
        print(f"Model already exists at {local_path}. Skipping download.")


def load_model(model: torch.nn.Module, model_path: str, map_location='cpu') -> Optional[torch.nn.Module]:
    if model is None:
        raise ValueError("A model instance must be provided.")
    print(f"Loading model weights from {model_path} ...")
    state_dict = torch.load(model_path, map_location=map_location, weights_only=True)
    model.load_state_dict(state_dict)
    print("Model loaded successfully.")
    return model


if __name__ == "__main__":
    url = "https://github.com/binarycode11/singular-points/raw/refs/heads/main/data/models/sp_map_fo_30.pth"
    local_path = "./models/singular-0.0.1.pth"

    download_model(url, local_path)

    # Exemplo: carregando em um modelo fictício
    # model = MyModel()
    # model = load_model(model, local_path)
