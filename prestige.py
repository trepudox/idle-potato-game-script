import bot_actions
from config import PRESTIGE_THRESHOLD
import logging


logger = logging.getLogger(__name__)


def try_prestige(potential_pp_magic_potatoes, potential_pp_no_magic_potatoes):
    """
    Verifica se a quantidade de PP potencial atinge o limite configurado e realiza o prestígio.
    """
    potential_pp = potential_pp_magic_potatoes if potential_pp_magic_potatoes > 0 else potential_pp_no_magic_potatoes

    if potential_pp >= PRESTIGE_THRESHOLD:
        logger.info(f"Opa! PP acumulado ({potential_pp}) atingiu o limite de {PRESTIGE_THRESHOLD}.")
        logger.info(f"Realizando prestígio com f{potential_pp} PPs")
        
        # Clica no botão de prestígio inicial
        clicked_prestige = bot_actions.click_template('prestige/prestige-now.png')
        
        if clicked_prestige:
            # Pop-up de confirmação abriu, clica no botão "Are you sure?" ou similar
            logger.info("Confirmando o Prestígio...")
            bot_actions.click_template('prestige/do-prestige-button.png')
            logger.info("Prestígio realizado com sucesso!")
            return True
        else:
            logger.warning("Botão de prestígio não encontrado na tela, mesmo com PP suficiente.")
            return False
    else:
        logger.info(f"PP atual: {potential_pp}. Faltam {PRESTIGE_THRESHOLD - potential_pp} para o prestígio.")
        return False