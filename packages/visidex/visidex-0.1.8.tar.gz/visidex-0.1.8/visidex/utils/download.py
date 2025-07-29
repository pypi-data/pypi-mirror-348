import os
import urllib

import torch

def load_model(model, weights_url, pretrained=True, map_location="cpu"):
    """
    Loads a PyTorch model from a URL using torch.hub.load_state_dict_from_url.

    Args:
        model: The PyTorch model to load weights into.
        weights_url: The URL of the pretrained weights.
        pretrained: Whether to load pretrained weights. Defaults to True.
        map_location: Device to map model parameters to. Defaults to "cpu".

    Returns:
        The loaded model.
    """
    if not model:
        raise ValueError("Model cannot be None")  # Raise an exception if the model is None

    if pretrained:
        try:
            state_dict = torch.hub.load_state_dict_from_url(
                weights_url,
                map_location=map_location,
                progress=True,
                check_hash=True,
            )
            model.load_state_dict(state_dict)
        except Exception as e:
            print(f"Error loading pretrained weights: {e}")
            return model  # Return the model even if loading fails

    model.eval()
    return model


def download_model(weights_url, local_folder):
    """
    Downloads a model from a URL to a local folder.

    Args:
        weights_url: The URL of the model weights.
        local_folder: The folder to store the model locally.
    """
    filename = weights_url.split('/')[-1]
    local_path = os.path.join(local_folder, filename)

    if not os.path.exists(local_path):
        print(f"Model weights not found locally at {local_path}. Downloading...")
        try:
            urllib.request.urlretrieve(weights_url, local_path)
            print(f"Model weights downloaded to {local_path}")
        except Exception as e:
            print(f"Error downloading model: {e}")
    else:
        print(f"Model weights found locally at {local_path}.")