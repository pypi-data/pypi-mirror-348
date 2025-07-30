# VisiDex: Keypoint Detection and Visual Retrieval Library

## Pacote detection
Contém classes e funções para detecção de keypoints e pontos singulares em imagens.
### Classes
- Detecção de keypoints usando o algoritmo REKD.

Exemplo de uso:
````
from visidex.detection import REKD

rd = REKD()
image = ...
keypoints = rd.detect(image)
````
- SingularPoints - Detecção de pontos singulares em imagens.
````
from visidex.detection import SingularPoints

sp = SingularPoints()
image = ...
points = sp.detect(image)
````
### apoio
- Python 3.9+
- PyTorch 2.1+
- Kornia 0.8.0+
- e2cnn 0.2.3+
- pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

