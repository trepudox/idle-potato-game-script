import logging
import bot_actions
import vision


logger = logging.getLogger(__name__)


def check_game_state():
    game_was_repaired = False

    logger.info("Checando estado do jogo...")

    # 1. Verifica se é necessário se reconectar
    if vision.find_template("reliability/reconnect-button.png"):
        logger.info("Reconnect button encontrado. Reconectando...")
        bot_actions.click_template("reliability/reconnect-button.png")
        game_was_repaired = True

    # 2. Verifica se o jogo está com algum popup
    # if vision.find_template("reliability/popup-box.png"):
    #     logger.info("Popup box encontrado. Fechando...")
    #     bot_actions.click_template("reliability/popup-box.png")
    #     game_was_repaired = True
    
    return game_was_repaired