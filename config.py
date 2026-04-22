from constants import *
import os

# Caminhos de Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Se a pasta não existir, cria
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)

# Configurações de Visão Computacional (OpenCV)
OPENCV_CONFIDENCE_THRESHOLD = 0.8  # Nível de confiança padrão (0 a 1) para encontrar imagens

DEFAULT_ACTION_DELAY = 1.5         # Tempo de espera padrão entre ações
DEFAULT_CLICK_DURATION = 0.1        # Duração do "click" (mouse down/up)

# Bounding Boxes para OCR
# Formato do MSS: {"top": y, "left": x, "width": w, "height": h}
RESOURCES_REGIONS = {
    POTATOES: {"top": 118, "left": 1800, "width": 98, "height": 18},
    GOLDEN_POTATOES: {"top": 144, "left": 1800, "width": 98, "height": 18},
    MAGIC_POTATOES: {"top": 170, "left": 1800, "width": 98, "height": 18},
    CASH: {"top": 196, "left": 1800, "width": 98, "height": 18},
    POTENTIAL_PP: {"top": 493, "left": 1800, "width": 98, "height": 18},
}

SELL_POTATOES_REGIONS = {
    POTATOES: {"top": 363, "left": 358, "width": 120, "height": 18},
    GOLDEN_POTATOES: {"top": 453, "left": 358, "width": 120, "height": 18},
}
