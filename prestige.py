from config import DEFAULT_ACTION_DELAY
from game_constants import *
import bot_actions
import logging


logger = logging.getLogger(__name__)


def try_prestige(potential_pp, try_prestige_flag, prestige_threshold):
    if potential_pp >= prestige_threshold and try_prestige_flag:
        bot_actions.press_key(TAB_BINDINGS[PRESTIGE])

        logger.info(f"Opa! Potential PP acumulado ({potential_pp}) atingiu o limite de {prestige_threshold}.")
        logger.info(f"Realizando prestígio com f{potential_pp} PPs")
        
        # Clica no botão de prestígio inicial
        clicked_prestige = bot_actions.click_template('prestige/prestige-now.png')
        
        if clicked_prestige:
            # Pop-up de confirmação abriu, clica no botão "Are you sure?" ou similar
            logger.info("Confirmando o Prestígio...")
            bot_actions.click_template('prestige/do-prestige-button.png')
            logger.info("Prestígio realizado com sucesso!")
            return True
        else:
            logger.warning("Botão de prestígio não encontrado na tela, mesmo com PP suficiente.")
            return False
    else:
        logger.info(f"Potential PP atual: {potential_pp}. Faltam {prestige_threshold - potential_pp} para o prestígio.")
        return False


def try_buy_prestige_upgrades(current_pp, ascension_cost):
    if current_pp <= 0 or ascension_cost <= 0:
        return
        
    logger.info("Verificando Upgrades de Prestígio (Fase 2 do Boss)...")
    bot_actions.press_key(TAB_BINDINGS[PRESTIGE])
    
    # Desce um pouquinho a tela
    logger.info("Rolando a tela para procurar os upgrades...")
    bot_actions.scroll_down(clicks=-600, delay=1.0)
    
    from config import PRESTIGE_UPGRADES_ANCHORS
    import vision
    from utils import extract_number
    import time
    
    for upgrade_name, config_data in PRESTIGE_UPGRADES_ANCHORS.items():
        template_path = config_data["template"]
        logger.info(f"Procurando a âncora do upgrade: {upgrade_name}")
        
        # Acha a imagem do ícone na tela
        loc = vision.find_template(template_path, threshold=0.8)
        if not loc:
            logger.warning(f"Ícone do {upgrade_name} não encontrado na tela.")
            continue
            
        x, y = loc
        
        # Monta a região do OCR baseada no deslocamento
        cost_region = {
            "top": int(y + config_data["cost_offset_y"]),
            "left": int(x + config_data["cost_offset_x"]),
            "width": config_data["cost_width"],
            "height": config_data["cost_height"]
        }
        
        limite_gasto = ascension_cost * 0.30
        
        while True:
            # Lê o custo
            cost_text = vision.read_text_from_region(cost_region, preprocess=True)
            cost = extract_number(cost_text)
            logger.info(f"Custo lido do {upgrade_name}: {cost} (Cru: '{cost_text}')")
            
            if cost == -1:
                logger.warning(f"Não foi possível ler o custo do {upgrade_name}. Parando de comprar este upgrade.")
                break

            if cost > config_data["max_cost"]:
                logger.info(f"O custo de {cost} é maior que o limite de {config_data["max_cost"]}. Parando de comprar este upgrade.")
                break

            if cost < limite_gasto:
                if current_pp >= cost:
                    logger.info(f"O custo de {cost} é menor que o limite ({limite_gasto}) e temos PP ({current_pp}). COMPRANDO!")
                    buy_x = x + config_data["buy_offset_x"]
                    buy_y = y + config_data["buy_offset_y"]
                    bot_actions.click_at(buy_x, buy_y, delay=0.5)
                    # Atualiza nosso current_pp para abater o custo
                    current_pp -= cost
                    time.sleep(DEFAULT_ACTION_DELAY) # Espera o jogo atualizar o texto de custo da próxima compra
                else:
                    logger.info(f"Preço excelente ({cost} < {limite_gasto}), mas não temos PP suficiente ({current_pp}).")
                    break
            else:
                logger.info(f"O upgrade {upgrade_name} está muito caro ({cost} >= limite de {limite_gasto}). Parando de comprar.")
                break
            
    # Volta o scroll para cima para não quebrar o clique do botão de prestige padrão se precisar
    bot_actions.scroll_up(clicks=500, delay=0.5)