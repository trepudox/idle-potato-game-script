from src.game_constants import *
from src.config import ASCENSION_REGIONS
from src import bot_actions
from src import vision
from src.utils import extract_number
import logging


logger = logging.getLogger(__name__)


def get_ascension_cost():
    """Abre a aba de Ascensão apenas para ler o custo atual."""
    logger.info("Checando custo de Ascensão atual...")
    bot_actions.press_key(TAB_BINDINGS[ASCENSION])
    
    ascension_cost_text = vision.read_text_from_region(ASCENSION_REGIONS[ASCENSION_COST], preprocess=True)
    cost = extract_number(ascension_cost_text)
    
    if cost != -1:
        logger.info(f"Custo de Ascensão atualizado para: {cost}")
    else:
        logger.warning(f"Falha ao ler o custo de Ascensão (texto lido: '{ascension_cost_text}')")
        
    return cost


def try_ascend(current_pp, try_ascension_flag, blessing_text):
    if not try_ascension_flag:
        return False
        
    logger.info("Tentando abrir a aba de Ascensão...")
    bot_actions.press_key(TAB_BINDINGS[ASCENSION])
    
    # Lê o custo na tela
    ascension_cost_text = vision.read_text_from_region(ASCENSION_REGIONS[ASCENSION_COST], preprocess=True)
    ascension_cost = extract_number(ascension_cost_text)
    
    logger.info(f"Custo de Ascensão lido: {ascension_cost} (Texto cru: '{ascension_cost_text}')")
    
    if ascension_cost == -1:
        logger.warning("Falha ao ler o custo de Ascensão. Verifique a região do OCR!")
        return False
        
    if current_pp >= ascension_cost:
        logger.info(f"UAU! Você tem CURRENT PP suficiente ({current_pp} >= {ascension_cost}). Iniciando Ascensão!")
        
        # 1. Procura pela benção usando OCR nas regiões definidas
        logger.info(f"Procurando pelo Blessing: {blessing_text} usando OCR...")
        blessing_found = False

        for key, region in ASCENSION_REGIONS.items():
            if key == ASCENSION_COST:
                continue
                
            # Lê o texto da região usando o OCR com pré-processamento
            read_text = vision.read_text_from_region(region, preprocess=True)
            logger.info(f"Lendo slot de blessing... OCR encontrou: '{read_text}'")
            
            # Se o texto da região corresponder à bênção que queremos (ignorando maiúsculas)
            # Removemos espaços em branco para evitar erros de leitura
            if blessing_text.replace(" ", "").lower() in read_text.replace(" ", "").lower():
                # Calcula o centro da região para clicar
                center_x = region["left"] + (region["width"] // 2)
                center_y = region["top"] + (region["height"] // 2)
                
                logger.info(f"Blessing '{blessing_text}' identificado por OCR! Clicando na coordenada ({center_x}, {center_y})")
                bot_actions.click_at(center_x, center_y)
                blessing_found = True
                break
                
        if blessing_found:
            # 2. Confirma a ascensão
            logger.info("Confirmando a Ascensão (botão final)...")
            clicked_ascend = bot_actions.click_template('ascension/ascend-button.png')
            
            if clicked_ascend:
                logger.info("Ascensão realizada com sucesso supremo! O jogo reseta com bônus!")
                return True
            else:
                logger.warning("Botão de confirmar Ascensão (ascend-button.png) não encontrado.")
        else:
            logger.warning(f"Blessing '{blessing_text}' não encontrado na tela pelo OCR.")
            
        return False
    else:
        logger.info(f"CURRENT PP insuficiente para ascender: {current_pp} / {ascension_cost}")
        return False