from game_constants import *
import vision
import bot_actions
import logging
import time


logger = logging.getLogger(__name__)


def try_buy_generator():
    bot_actions.press_key(TAB_BINDINGS[GENERATORS])

    if vision.find_template('generators/slots-full.png', threshold=0.8):
        logger.info("Slots cheios! Não é possível comprar mais geradores.")
        return

    # Não precisamos mais do current_cash para lógica, mas mantemos na assinatura caso precise depois
    logger.info("Descendo até o final da lista de geradores...")
    # Da 3 scrolls fortes pra baixo para garantir que chegou no fim da lista
    for _ in range(3):
        bot_actions.scroll_down(clicks=-1000, delay=0.3)
    time.sleep(0.5) # Espera a tela estabilizar

    max_scrolls = 6 # Limite para não ficar em loop infinito subindo a tela
    
    for scroll_idx in range(max_scrolls):
        # Encontra apenas os botões de COMPRA ATIVOS (verdes/disponíveis)
        buy_locations = vision.find_all_templates('generators/buy-generator.png', threshold=0.8, min_distance=30)
        
        if buy_locations:
            logger.info(f"Encontrados {len(buy_locations)} botões de compra ativos na tela {scroll_idx + 1}.")
            
            # Como a tela atual é o mais próximo possível do final da lista,
            # e o jogo ordena do mais barato (topo) pro mais caro (fundo),
            # o gerador mais caro que podemos pagar é o que tem o maior valor de Y (mais pra baixo na tela)!
            
            # Ordena as localizações pelo eixo Y de forma decrescente (do maior Y pro menor Y)
            buy_locations.sort(key=lambda loc: loc[1], reverse=True)
            best_generator_x, best_generator_y = buy_locations[0]
            
            logger.info("Comprando o gerador mais caro disponível!")
            bot_actions.click_at(best_generator_x, best_generator_y)
            time.sleep(1) # Tempo pro jogo registrar a compra
            return # Sai da função
            
        # Se chegou aqui, não achou nenhum botão acessível nesta tela. Rola um pouco pra cima.
        logger.info("Nenhum gerador disponível nesta parte da lista. Rolando para cima...")
        bot_actions.scroll_up(clicks=500, delay=0.6)
        
    logger.info("Varreu toda a lista de baixo para cima e não encontrou geradores disponíveis.")