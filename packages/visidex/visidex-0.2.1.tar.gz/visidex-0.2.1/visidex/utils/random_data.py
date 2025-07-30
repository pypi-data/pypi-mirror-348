import gc
import logging
import random
import numpy as np
import torch
import kornia

logger = logging.getLogger("Utils")

class AugmentationGenerator:
    def __init__(self, n_variations, augmentation_sequence=None):
        """
        Gera variações de augmentações a partir de uma sequência definida ou padrão.

        Args:
            n_variations (int): Número de variações a serem geradas.
            augmentation_sequence (AugmentationSequential, opcional): Uma sequência customizada de augmentações.
        """
        if augmentation_sequence is None:
            augmentation_sequence = kornia.augmentation.AugmentationSequential(
                kornia.augmentation.RandomAffine(degrees=360, translate=(0.2, 0.2), scale=(0.95, 1.05), shear=10,
                                                 p=0.8),
                kornia.augmentation.RandomPerspective(0.2, p=0.7),
                kornia.augmentation.RandomBoxBlur((4, 4), p=0.5),
                data_keys=[
                    kornia.constants.DataKey.INPUT,
                    kornia.constants.DataKey.MASK,
                    kornia.constants.DataKey.KEYPOINTS
                ],
                same_on_batch=True,
            )

        self.augmentation_sequence = augmentation_sequence
        self.n_variations = n_variations
        self.param_list = []
        self.current_index = 0

    def generate_variations(self, image, mask, keypoints):
        """
        Gera múltiplas variações de augmentações e coleta seus parâmetros.
        """
        for _ in range(self.n_variations):
            # Apenas executa a sequência de augmentação e salva os parâmetros gerados
            self.augmentation_sequence(image, mask, keypoints)
            self.param_list.append(self.augmentation_sequence._params)

    def __iter__(self):
        self.current_index = 0  # Resetar o índice a cada nova iteração
        return self

    def __next__(self):
        """
        Retorna a próxima variação de parâmetros de augmentação.
        A iteração será circular.
        """
        result = self.param_list[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.param_list)
        return result

    def reset(self):
        """Método para resetar o estado do gerador de augmentação."""
        self.current_index = 0  # Reseta o índice de iteração


def set_seed(seed):
    logger.debug(f"Setting seed to {seed}")
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def check_and_clear_memory():
    logger.debug(f'Memória alocada antes da limpeza: {torch.cuda.memory_allocated()} bytes')
    logger.debug(f'Memória reservada antes da limpeza: {torch.cuda.memory_reserved()} bytes')

    torch.cuda.empty_cache()
    gc.collect()

    logger.debug(f'Memória alocada após limpeza: {torch.cuda.memory_allocated()} bytes')
    logger.debug(f'Memória reservada após limpeza: {torch.cuda.memory_reserved()} bytes')