from constants import *
import time
import sys
import logging
from trepudox_py_utils.logging import configure_logger
import vision
import bot_actions
from config import RESOURCES_REGIONS

configure_logger()
logger = logging.getLogger(__name__)

def extract_number(text):
    """Função utilitária para limpar o texto lido pelo OCR e converter para inteiro com multiplicadores"""
    text = text.replace(" ", "").strip()
    if not text:
        return -1
        
    for suffix, multiplier in MULTIPLIERS.items():
        if text.lower().endswith(suffix.lower()):
            number_part = text[:-len(suffix)]
            number_part = number_part.replace(',', '.')
            # Remove qualquer caracter inválido da parte numérica (ex: erros pequenos do OCR)
            clean_num = ''.join(c for c in number_part if c.isdigit() or c == '.')
            if clean_num:
                try:
                    return int(float(clean_num) * multiplier)
                except ValueError as e:
                    logger.warning(f"Erro ao converter número: {e}")
                    pass
            break
            
    # Fallback se não tiver sufixo
    clean_text = ''.join(filter(str.isdigit, text))
    if clean_text:
        return int(clean_text)

    return -1


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
            # 1. Checa o estado (lê dinheiro/batatas)
            resources_dict = check_resources()
            
            # 2. Exemplo de lógica (O usuário deve adaptar para as regras do seu jogo)
            # if money > 1000:
            #     logger.info("Temos bastante dinheiro, tentando comprar upgrade!")
            #     if bot_actions.click_template("btn_upgrade.png"):
            #         logger.info("Upgrade comprado.")
            
            # 3. Exemplo de checar aba de prestígio
            # if potatoes > 5000:
            #     logger.info("Hora do prestígio!")
            #     if bot_actions.click_template("tab_prestige.png"):
            #         bot_actions.click_template("btn_do_prestige.png")
            
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
