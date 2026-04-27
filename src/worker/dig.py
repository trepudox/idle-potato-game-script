from src import bot_actions
import logging

logger = logging.getLogger(__name__)

def try_dig():
    logger.info("Tentando acessar a aba de Dig...")
    
    # 1. Clica na aba de Dig (já que não tem atalho no teclado)
    clicked_tab = bot_actions.click_template('dig/dig-tab-button.png')
    
    if clicked_tab:
        logger.info("Aba de Dig aberta. Clicando no Autodig...")
        
        # 2. Clica no botão para iniciar a escavação
        clicked_dig = bot_actions.click_template('dig/dig-button.png', threshold=0.95)
        
        if clicked_dig:
            logger.info("Autodig ativado com sucesso!")
        else:
            logger.warning("Botão de Autodig não encontrado na tela.")
    else:
        logger.warning("Não foi possível encontrar o botão da aba Dig.")