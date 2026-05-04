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
    found_popups = vision.find_all_templates(popup_templates)
    if len(found_popups) > 0:
        logger.info("Popup box encontrado. Fechando...")
        bot_actions.click_template("reliability/popup-box.png", threshold=0.9)
        game_was_repaired = True
    
    return game_was_repaired