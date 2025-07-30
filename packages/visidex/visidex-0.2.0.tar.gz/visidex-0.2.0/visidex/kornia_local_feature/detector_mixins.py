import torch
from torch import nn, Tensor
from kornia.feature import (
    MultiResolutionDetector, PassLAF, LAFOrienter, LAFAffNetShapeEstimator
)
from kornia.feature.keynet import KeyNetDetector
from visidex.detection import REKD
from visidex.utils import get_config_rekd,get_config_singular,load_model,download_file
from visidex.detection import SingularPoints


class BaseDetector(nn.Module):
    """Classe base para inicialização de detectores."""

    def initialize_detector(self, num_features: int, size_laf: int = 19) -> nn.Module:
        """Método que deve ser implementado para criar o detector."""
        raise NotImplementedError


class KeyNetDetectorMixin(BaseDetector):
    """Mixin para o detector KeyNet."""

    def initialize_detector(self, num_features: int, size_laf: int = 19) -> nn.Module:
        return KeyNetDetector(
            pretrained=True,
            num_features=num_features,
            ori_module=PassLAF() if self.upright else LAFOrienter(size_laf),
            aff_module=LAFAffNetShapeEstimator(preserve_orientation=self.upright).eval(),
            keynet_conf=self.config,
        ).to(self.device).eval()


class REKDetectorMixin(BaseDetector):
    """Mixin para o detector REKD."""

    def initialize_detector(self, num_features: int, size_laf: int = 19) -> nn.Module:
        class REKDetector(nn.Module):
            def __init__(self, params, device: torch.device) -> None:
                super().__init__()
                self.model = REKD(params, device).to(device).eval()

                url = "https://github.com/binarycode11/visidex/raw/refs/heads/main/data/model/rekd_model.pt"

                local_path = "./models/rekd-0.0.1.pt"
                download_file(url, local_path)
                self.model = load_model(self.model, local_path, map_location=device)
                self.model.eval()

            def forward(self, x: Tensor) -> Tensor:
                return self.model(x)[0]

        args = get_config_rekd(jupyter=True)
        args.device = self.device

        return MultiResolutionDetector(
            REKDetector(args, args.device),
            num_features=num_features,
            config=self.config["Detector_conf"],
            ori_module=LAFOrienter(size_laf),
        ).to(self.device)


class SingularPointDetectorMixin(BaseDetector):
    """Mixin para o detector SingularPoint."""

    def initialize_detector(self, num_features: int, size_laf: int = 19) -> nn.Module:
        class SingularPointDetector(nn.Module):
            def __init__(self, params, device: torch.device) -> None:
                super().__init__()
                self.model = SingularPoints(params).to(device)

                url = "https://github.com/binarycode11/visidex/raw/refs/heads/main/data/model/sp_map_fo_30.pth" # './model/models/sp2_85.pth'
                local_path = "./models/singular-0.0.1.pth"
                download_file(url, local_path)
                self.model= load_model(self.model, local_path, map_location=device)
                self.model.eval()

            def forward(self, x):
                return self.model(x)[1]

        args = get_config_singular(jupyter=True)
        args.num_channels = 1
        args.device = self.device
        return MultiResolutionDetector(
            SingularPointDetector(args, args.device),
            num_features=num_features,
            config=self.config["Detector_conf"],
            ori_module=LAFOrienter(size_laf),
        )
