import time
import logging
from src import bot_actions, vision


logger = logging.getLogger(__name__)


popup_templates = [
    "reliability/welcome-back-popup.png",
    "reliability/login-rewards-popup.png",
]

reconnect_templates = [
    "reliability/reconnect-button.png",
    "reliability/retry-button.png",
]

def check_game_state():
    game_was_repaired = False

    logger.info("Checando estado do jogo...")

    # 1. Verifica se é necessário se reconectar
    for template in reconnect_templates:
        if vision.find_template(template, threshold=0.9):
            logger.info(f"Reconnect button {template} encontrado. Reconectando...")
            bot_actions.click_template(template, threshold=0.9)
            game_was_repaired = True
            time.sleep(3)

    # 2. Verifica se o jogo está com algum popup
    for template in popup_templates:
        if vision.find_template(template, threshold=0.9):
            logger.info(f"Popup {template} encontrado. Fechando...")
            bot_actions.click_template("reliability/close-popup-button.png", threshold=0.95)
            game_was_repaired = True
            time.sleep(3)
    
    return game_was_repaired