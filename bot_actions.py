import pyautogui
import pydirectinput
import time
import logging
import vision
from config import DEFAULT_ACTION_DELAY


logger = logging.getLogger(__name__)


# Configurações globais do PyAutoGUI
pyautogui.PAUSE = 0.25  # Pequena pausa após cada ação do pyautogui
pyautogui.FAILSAFE = True  # Move o mouse para o canto da tela para abortar


def press_key(key, delay=DEFAULT_ACTION_DELAY):
    """Pressiona uma tecla."""
    logger.info(f"Pressionando tecla '{key}'")
    # Jogos costumam ignorar o press() rápido do pyautogui
    # Usar keyDown e keyUp com um tempinho garante que o jogo registre
    pydirectinput.keyDown(key)
    time.sleep(0.1) # Segura a tecla por 100ms
    pydirectinput.keyUp(key)
    time.sleep(delay)


def click_at(x, y, delay=DEFAULT_ACTION_DELAY):
    """Move o mouse e clica em uma coordenada."""
    logger.info(f"Clicando na coordenada ({x}, {y})")
    pyautogui.moveTo(int(x), int(y), duration=0.175, tween=pyautogui.easeInOutQuad)
    time.sleep(0.025)
    
    # O SEGREDO ESTÁ AQUI: O jogo só atualiza o cursor quando recebe movimento "físico" relativo.
    # Vamos injetar um movimento direto no driver do Windows (1 pixel para o lado e voltando)
    import ctypes
    # 0x0001 = MOUSEEVENTF_MOVE (Movimento Relativo Real)
    ctypes.windll.user32.mouse_event(0x0001, 1, 1, 0, 0)
    time.sleep(0.025)
    ctypes.windll.user32.mouse_event(0x0001, -1, -1, 0, 0)
    time.sleep(0.025) # Espera o jogo transformar o cursor em "mãozinha"

    pydirectinput.mouseDown()
    time.sleep(0.1)
    pydirectinput.mouseUp()
    
    time.sleep(delay)


def click_template(template_name, threshold=0.8, delay=DEFAULT_ACTION_DELAY):
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


def scroll_down(clicks=-500, delay=0.375):
    """Rola a tela do jogo para baixo usando eventos de hardware para garantir que funciona em jogos."""
    logger.info("Rolando a tela para baixo...")
    import ctypes
    # 0x0800 = MOUSEEVENTF_WHEEL
    # cliques negativos rolam pra baixo
    ctypes.windll.user32.mouse_event(0x0800, 0, 0, clicks, 0)
    time.sleep(delay)


def scroll_up(clicks=500, delay=0.375):
    """Rola a tela do jogo para cima usando eventos de hardware para garantir que funciona em jogos."""
    logger.info("Rolando a tela para cima...")
    import ctypes
    # 0x0800 = MOUSEEVENTF_WHEEL
    # cliques positivos rolam pra cima
    ctypes.windll.user32.mouse_event(0x0800, 0, 0, clicks, 0)
    time.sleep(delay)
