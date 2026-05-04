import time
import logging
from src import bot_actions, vision


logger = logging.getLogger(__name__)


popup_templates = [
    "reliability/welcome-back-popup.png",
]

def check_game_state():
    game_was_repaired = False

    logger.info("Checando estado do jogo...")

    # 1. Verifica se é necessário se reconectar
    if vision.find_template("reliability/reconnect-button.png"):
        logger.info("Reconnect button encontrado. Reconectando...")
        bot_actions.click_template("reliability/reconnect-button.png")
        game_was_repaired = True

    # 2. Verifica se o jogo está com algum popup
    for template in popup_templates:
        if vision.find_template(template, threshold=0.9):
            logger.info(f"Popup {template} encontrado. Fechando...")
            bot_actions.click_template(template, threshold=0.9)
            game_was_repaired = True
            time.sleep(1)
    
    return game_was_repaired