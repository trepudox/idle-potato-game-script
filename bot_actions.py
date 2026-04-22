import pyautogui
import time
import logging
import vision
from config import DEFAULT_CLICK_DELAY, DEFAULT_CLICK_DURATION


logger = logging.getLogger(__name__)


# Configurações globais do PyAutoGUI
pyautogui.PAUSE = 0.15  # Pequena pausa após cada ação do pyautogui
pyautogui.FAILSAFE = True  # Move o mouse para o canto da tela para abortar


def click_at(x, y, delay=DEFAULT_CLICK_DELAY):
    """Move o mouse e clica em uma coordenada."""
    logger.info(f"Clicando na coordenada ({x}, {y})")
    pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    pyautogui.click(duration=DEFAULT_CLICK_DURATION)
    time.sleep(delay)


def click_template(template_name, threshold=0.8, delay=DEFAULT_CLICK_DELAY):
    """
    Procura uma imagem na tela e clica nela se encontrar.
    Retorna True se clicou, False se não encontrou.
    """
    coords = vision.find_template(template_name, threshold=threshold)
    if coords:
        x, y = coords
        logger.info(f"Encontrou template '{template_name}' em ({x}, {y})")
        click_at(x, y, delay)
        return True
    
    logger.debug(f"Não encontrou template '{template_name}' na tela.")
    return False
