import prestige
import generators
import sell_potatoes
from constants import *
import time
import sys
import logging
from trepudox_py_utils.logging import configure_logger
import vision
import bot_actions
from config import RESOURCES_REGIONS
from utils import extract_number


configure_logger()
logger = logging.getLogger(__name__)


def check_resources():
    """Lê os valores principais da tela."""
    logger.info("Checando recursos atuais")
    
    potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[POTATOES])
    golden_potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[GOLDEN_POTATOES])
    magic_potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[MAGIC_POTATOES])
    cash_text = vision.read_text_from_region(RESOURCES_REGIONS[CASH])[1:]
    potential_pp_text = vision.read_text_from_region(RESOURCES_REGIONS[POTENTIAL_PP])

    # logger.info(f"cash_text: {cash_text}")
    # logger.info(f"potatoes_text: {potatoes_text}")
    # logger.info(f"golden_potatoes_text: {golden_potatoes_text}")
    # logger.info(f"magic_potatoes_text: {magic_potatoes_text}")
    # logger.info(f"pontential_pp_text: {potential_pp_text}")

    potatoes = extract_number(potatoes_text)
    golden_potatoes = extract_number(golden_potatoes_text)
    magic_potatoes = extract_number(magic_potatoes_text)
    cash = extract_number(cash_text)
    pontential_pp = extract_number(potential_pp_text)

    # logger.info(f"cash atual: {cash}")
    # logger.info(f"potatoes atuais: {potatoes}")
    # logger.info(f"golden_potatoes atuais: {golden_potatoes}")
    # logger.info(f"magic_potatoes atuais: {magic_potatoes}")
    # logger.info(f"pontential_pp atual: {pontential_pp}")
    
    return {
        CASH: cash,
        POTATOES: potatoes,
        GOLDEN_POTATOES: golden_potatoes,
        MAGIC_POTATOES: magic_potatoes,
        POTENTIAL_PP: pontential_pp
    }

def main_loop():
    logger.info("Iniciando Bot do Idle Potato...")
    logger.info("Pressione Ctrl+C no terminal ou jogue o mouse para o canto da tela (FailSafe) para parar.")
    
    try:
        while True:
            # 1. Checa o estado (lê dinheiro/batatas/pp)
            bot_actions.press_key(TAB_BINDINGS[HOME])
            resources_dict = check_resources()

            # 2. Tenta vender batatas
            bot_actions.press_key(TAB_BINDINGS[SELL_POTATOES])
            sell_potatoes.try_sell_potatoes()

            # 3. Tenta comprar geradores
            bot_actions.press_key(TAB_BINDINGS[GENERATORS])
            generators.try_buy_generator()

            # 4. Checa o estado (lê dinheiro/batatas/pp)
            bot_actions.press_key(TAB_BINDINGS[HOME])
            resources_dict = check_resources()

            # 5. Tenta fazer prestige
            bot_actions.press_key(TAB_BINDINGS[PRESTIGE])
            prestige.try_prestige()

            # Pausa para não sobrecarregar a CPU
            logger.info("Aguardando próximo ciclo...")
            logger.info("-----------------------------------------")
            time.sleep(5)
            
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário (Ctrl+C). Encerrando...")
        sys.exit(0)
    except Exception as e:
        logger.exception("Ocorreu um erro inesperado no loop principal.")


if __name__ == "__main__":
    main_loop()
