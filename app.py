from game_constants import BLESSING_OF_ABUNDANCE
import ascension
import dig
import shop
from config import DEFAULT_ACTION_DELAY
import prestige
import ascension
import generators
import sell_potatoes
from game_constants import *
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


PRESTIGE_THRESHOLD = 35
TRY_PRESTIGE = True
TRY_ASCENSION = True
ASCENSION_BLESSING = BLESSING_OF_ABUNDANCE


def check_resources():
    """Lê os valores principais da tela."""
    logger.info("Checando recursos atuais")
    
    potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[POTATOES])
    golden_potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[GOLDEN_POTATOES])
    magic_potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[MAGIC_POTATOES])
    cash_text = vision.read_text_from_region(RESOURCES_REGIONS[CASH])[1:]
    current_pp_text = vision.read_text_from_region(RESOURCES_REGIONS[CURRENT_PP], preprocess=True)
    potential_pp_text = vision.read_text_from_region(RESOURCES_REGIONS[POTENTIAL_PP], preprocess=True)

    logger.info(f"current_pp_text: {current_pp_text}")
    logger.info(f"pontential_pp_text: {potential_pp_text}")

    potatoes = extract_number(potatoes_text)
    golden_potatoes = extract_number(golden_potatoes_text)
    magic_potatoes = extract_number(magic_potatoes_text)
    cash = extract_number(cash_text)
    current_pp = extract_number(current_pp_text)
    potential_pp = extract_number(potential_pp_text)

    logger.info(f"current_pp atual: {current_pp}")
    logger.info(f"pontential_pp atual: {potential_pp}")
    time.sleep(DEFAULT_ACTION_DELAY)

    return {
        CASH: cash,
        POTATOES: potatoes,
        GOLDEN_POTATOES: golden_potatoes,
        MAGIC_POTATOES: magic_potatoes,
        CURRENT_PP: current_pp,
        POTENTIAL_PP: potential_pp,
    }

def main_loop():
    logger.info("Iniciando Bot do Idle Potato...")
    logger.info("Pressione Ctrl+C no terminal ou jogue o mouse para o canto da tela (FailSafe) para parar.")
    
    try:
        import ctypes
        while True:
            # --- KILL SWITCH DE EMERGÊNCIA (Segurar ESC) ---
            # 0x1B é o código da tecla ESC no Windows. 0x8000 verifica se a tecla está sendo segurada.
            if ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000:
                logger.warning("Botão ESC segurado! Abortando o bot de emergência.")
                break

            # 1. Tenta vender batatas
            potatoes_sold, golden_potatoes_sold = sell_potatoes.try_sell_potatoes()

            # 2. Checa o estado (lê dinheiro/batatas/pp)
            resources_dict = check_resources()

            # 3. Busca o custo de ascensão para calcular o limite de gastos no Prestígio
            ascension_cost = ascension.get_ascension_cost()

            # 4. Tenta fazer prestige
            prestiged = prestige.try_prestige(resources_dict[POTENTIAL_PP], TRY_PRESTIGE, PRESTIGE_THRESHOLD)
            
            # 5. Se prestiged, tenta fazer ascensão, se não, compra upgrades
            if prestiged:
                resources_dict = check_resources()
                
                if resources_dict[CURRENT_PP] >= ascension_cost:
                    ascension.try_ascend(resources_dict[CURRENT_PP], TRY_ASCENSION, ASCENSION_BLESSING)
                    continue

                prestige.try_buy_prestige_upgrades(resources_dict[CURRENT_PP], ascension_cost)

            # 4. Tenta comprar geradores se vender batatas de ouro
            if golden_potatoes_sold:
                generators.try_buy_generator()
            else:
                logger.info("Batatas de ouro nao foram vendidas, pulando compra de geradores")

            # 5. Tenta comprar intes do shop
            shop.try_buy_shop_items()

            # 6. Tenta escavar antes do sleep
            # Nao tem binding!!! o dig.py clica no botao pra começar a escavar
            dig.try_dig()

            # 7. Alterna para a próxima conta (Múltiplas instâncias)
            logger.info("Ciclo concluído nesta conta. Alternando para a próxima...")
            logger.info("-----------------------------------------")
            bot_actions.switch_instance()
            
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário (Ctrl+C). Encerrando...")
        sys.exit(0)
    except Exception as e:
        logger.exception("Ocorreu um erro inesperado no loop principal.")


if __name__ == "__main__":
    main_loop()
