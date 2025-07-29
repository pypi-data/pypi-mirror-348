import torch
from typing import Optional
from kornia.feature import LocalFeature
from .detector_mixins import KeyNetDetectorMixin, REKDetectorMixin, SingularPointDetectorMixin
from .descriptor_mixins import SIFTDescriptorMixin, SosNetDescriptorMixin, HardNetDescriptorMixin

CPU_DEVICE = torch.device("cpu")

class LocalFeatureCombinationBase(LocalFeature):
    """Base para combinações de detector e descritor locais."""

    DEFAULT_CONFIG = {'num_filters': 8, 'num_levels': 3, 'kernel_size': 5,
                      'Detector_conf': {'nms_size': 5, 'pyramid_levels': 0, 'up_levels': 0, 'scale_factor_levels': 1.3,
                                        's_mult': 12.0}}
    def __init__(
        self,
        num_features: int = 200,
        upright: bool = False,
        device: torch.device = CPU_DEVICE,
        config: Optional[dict] = None
    ) -> None:
        super().__init__(detector=None, descriptor=None)
        self.upright, self.device, self.config = upright, device, config or self.DEFAULT_CONFIG
        self.to(self.device)

        if all(hasattr(self, method) for method in ('initialize_detector', 'initialize_descriptor')):
            self.detector, self.descriptor = self.initialize_detector(num_features), self.initialize_descriptor()


class KeyNetFeatureSIFT(LocalFeatureCombinationBase, KeyNetDetectorMixin, SIFTDescriptorMixin):
    """Combina o detector KeyNet com o descritor SIFT."""
    DEFAULT_CONFIG = {'num_filters': 8, 'num_levels': 3, 'kernel_size': 5,
                      'Detector_conf': {'nms_size': 5, 'pyramid_levels': 2, 'up_levels': 2, 'scale_factor_levels': 1.3,
                                        's_mult': 12.0}}
    pass


class KeyNetFeatureSosNet(LocalFeatureCombinationBase, KeyNetDetectorMixin, SosNetDescriptorMixin):
    """Combina o detector KeyNet com o descritor SOSNet."""
    DEFAULT_CONFIG = {'num_filters': 8, 'num_levels': 3, 'kernel_size': 5,
                      'Detector_conf': {'nms_size': 5, 'pyramid_levels': 2, 'up_levels': 2, 'scale_factor_levels': 1.3,
                                        's_mult': 12.0}}
    pass


class REKDSosNet(LocalFeatureCombinationBase, REKDetectorMixin, SosNetDescriptorMixin):
    """Combina o detector REKD com o descritor SOSNet."""
    pass


class SingularPointSosNet(LocalFeatureCombinationBase, SingularPointDetectorMixin, SosNetDescriptorMixin):
    """Combina o detector SingularPoint com o descritor SOSNet."""
    pass


class REKDHardNet(LocalFeatureCombinationBase, REKDetectorMixin, HardNetDescriptorMixin):
    """Combina o detector REKD com o descritor HardNet."""
    pass


class SingularPointHardNet(LocalFeatureCombinationBase, SingularPointDetectorMixin, HardNetDescriptorMixin):
    """Combina o detector SingularPoint com o descritor HardNet."""
    pass
