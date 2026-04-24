from game_constants import *
import time
import logging
import bot_actions
import vision

logger = logging.getLogger(__name__)

# Controle de tempo (cooldown) da loja
last_shop_visit = 0
# SHOP_COOLDOWN_SECONDS = 240  # 4 minutos
SHOP_COOLDOWN_SECONDS = 5  # 4 minutos

# Templates dos botões de compra disponíveis
SHOP_TEMPLATES = [
    'shop/buy-golden-potato.png',
    'shop/buy-money.png',
    'shop/buy-potato.png'
]

def try_buy_shop_items():
    global last_shop_visit
    bot_actions.press_key(TAB_BINDINGS[SHOP])
    
    current_time = time.time()
    
    # Verifica se o cooldown de 5 minutos já passou
    if current_time - last_shop_visit < SHOP_COOLDOWN_SECONDS:
        time_left = int(SHOP_COOLDOWN_SECONDS - (current_time - last_shop_visit))
        logger.info(f"Loja em cooldown. Faltam {time_left} segundos para a próxima visita.")
        return
        
    logger.info("Verificando itens disponíveis na loja...")
    
    items_bought = 0
    
    # Procura e clica em todos os itens usando os 3 templates
    for template_path in SHOP_TEMPLATES:
        # Procuramos por todas as ocorrências deste template na tela
        locations = vision.find_all_templates(template_path, threshold=0.9, min_distance=30)
        
        if locations:
            logger.info(f"Encontrados {len(locations)} itens do tipo '{template_path}'.")
            for x, y in locations:
                logger.info(f"Comprando item no shop em ({x}, {y})")
                bot_actions.click_at(x, y)
                items_bought += 1
                
    if items_bought > 0:
        logger.info(f"Total de {items_bought} itens comprados na loja desta vez.")
    else:
        logger.info("Nenhum item disponível para compra na loja agora.")
        
    # Atualiza o tempo da última visita, independentemente de ter comprado algo ou não
    last_shop_visit = time.time()