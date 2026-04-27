from src.game_constants import *
import os

# Caminhos de Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "src", "templates")

# Se a pasta não existir, cria
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)

# Configurações de Visão Computacional (OpenCV)
OPENCV_CONFIDENCE_THRESHOLD = 0.8  # Nível de confiança padrão (0 a 1) para encontrar imagens

DEFAULT_ACTION_DELAY = 0.2         # Tempo de espera padrão entre ações
DEFAULT_CLICK_DURATION = 0.1        # Duração do "click" (mouse down/up)

# Bounding Boxes para OCR
# Formato do MSS: {"top": y, "left": x, "width": w, "height": h}
RESOURCES_REGIONS = {
    POTATOES: {"top": 118, "left": 1800, "width": 98, "height": 18},
    GOLDEN_POTATOES: {"top": 144, "left": 1800, "width": 98, "height": 18},
    MAGIC_POTATOES: {"top": 170, "left": 1800, "width": 98, "height": 18},
    CASH: {"top": 196, "left": 1800, "width": 98, "height": 18},
    CURRENT_PP: {"top": 467, "left": 1835, "width": 60, "height": 18},
    POTENTIAL_PP: {"top": 493, "left": 1835, "width": 60, "height": 18},
}

SELL_POTATOES_REGIONS = {
    POTATOES: {"top": 363, "left": 358, "width": 120, "height": 18},
    GOLDEN_POTATOES: {"top": 453, "left": 358, "width": 120, "height": 18},
}

ASCENSION_REGIONS = {
    ASCENSION_COST: {"top": 104, "left": 875, "width": 60, "height": 49},
    BLESSING_OF_ABUNDANCE: {"top": 210, "left": 370, "width": 175, "height": 20},
    BLESSING_OF_THE_PRESTIGE: {"top": 325, "left": 370, "width": 175, "height": 20},
    BLESSING_OF_THE_THRIFTY: {"top": 438, "left": 370, "width": 175, "height": 20},
    BLESSING_OF_THE_GOLDEN: {"top": 550, "left": 370, "width": 175, "height": 20},
    BLESSING_OF_THE_COLLECTOR: {"top": 663, "left": 370, "width": 175, "height": 20},
}

# Configurações de Âncora Visual para a Fase 2 (Upgrades de Prestígio)
# Como a tela 'scrolla', nós achamos a imagem do ícone e usamos os offsets (X, Y) para ler o custo e clicar em comprar!
PRESTIGE_UPGRADES_ANCHORS = {
    STARTER_SEEDLING: {
        "template": "prestige/starter-seedlings-upgrade-icon.png",
        "cost_offset_x": 200,
        "cost_offset_y": 8,
        "cost_width": 125,
        "cost_height": 15,
        "buy_offset_x": 1110,
        "buy_offset_y": 0,
        "max_cost": 1
    },
    GENERATOR_BONUS: {
        "template": "prestige/generator-bonus-upgrade-icon.png",
        # Onde a caixa do custo fica em relação ao ícone?
        "cost_offset_x": 226,
        "cost_offset_y": 5,
        "cost_width": 125,
        "cost_height": 15,
        # Onde o botão de comprar fica em relação ao ícone?
        "buy_offset_x": 1110,
        "buy_offset_y": 0,
        "max_cost": 1000
    },
    PRESTIGE_MASTERY: {
        "template": "prestige/prestige-mastery-upgrade-icon.png",
        "cost_offset_x": 214,
        "cost_offset_y": 7,
        "cost_width": 125,
        "cost_height": 15,
        "buy_offset_x": 1110,
        "buy_offset_y": 0,
        "max_cost": 200
    },
    BULK_DISCOUNTS: {
        "template": "prestige/bulk-discounts-upgrade-icon.png",
        "cost_offset_x": 260,
        "cost_offset_y": 8,
        "cost_width": 125,
        "cost_height": 15,
        "buy_offset_x": 1110,
        "buy_offset_y": 0,
        "max_cost": 80
    },
    GOLDEN_IRRIGATION: {
        "template": "prestige/golden-irrigation-upgrade-icon.png",
        "cost_offset_x": 248,
        "cost_offset_y": 8,
        "cost_width": 125,
        "cost_height": 15,
        "buy_offset_x": 1110,
        "buy_offset_y": 0,
        "max_cost": 30
    },
}
