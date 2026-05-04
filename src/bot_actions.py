import pyautogui
import pydirectinput
import time
import logging
from src import vision
from src.config import DEFAULT_ACTION_DELAY, OPENCV_CONFIDENCE_THRESHOLD


logger = logging.getLogger(__name__)


# Configurações globais do PyAutoGUI
pyautogui.PAUSE = 0.25  # Pequena pausa após cada ação do pyautogui
pyautogui.FAILSAFE = False  # Desativado: o FailSafe antigo atrapalha o multi-instâncias. Usaremos a tecla ESC.


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


def click_template(template_name, threshold=OPENCV_CONFIDENCE_THRESHOLD, delay=DEFAULT_ACTION_DELAY):
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


def switch_instance():
    """
    Alterna para a instância mais antiga do jogo aberta usando Windows + Tab.
    O Windows + Tab organiza as janelas da mais recente (topo esquerda) para a mais antiga (baixo direita).
    Ao clicar na ÚLTIMA janela encontrada, garantimos o ciclo contínuo perfeito entre 3+ instâncias.
    """
    logger.info("Buscando próxima instância do jogo...")
    
    # Aciona a visão de tarefas do Windows
    pyautogui.hotkey('win', 'tab')
    time.sleep(0.5)  # Tempo para a animação do Windows terminar e os ícones renderizarem
    
    # Encontra as miniaturas das janelas do jogo
    # Threshold um pouco menor pois miniaturas podem perder resolução
    locations = vision.find_all_templates('windows-tab/roblox-window-name.png', threshold=0.7)
    
    if locations:
        logger.info(f"Encontradas {len(locations)} janelas do jogo abertas.")
        
        # Ordena as coordenadas:
        # Primeiro por Y (linha, de cima pra baixo). 
        # Para coordenadas na mesma linha (diferença de Y pequena), ordena por X (esquerda pra direita).
        # A matemática: agrupamos linhas num intervalo de ~50 pixels de tolerância
        locations.sort(key=lambda loc: (loc[1] // 50, loc[0]))
        
        # A janela menos usada (que deve ser jogada agora) é sempre a ÚLTIMA da lista
        target_x, target_y = locations[-1]
        
        logger.info("Alternando para a janela mais inativa...")
        # Clica para focar
        pyautogui.moveTo(int(target_x), int(target_y), duration=0.2)
        pydirectinput.click()
        
        # Tempo pro jogo voltar a focar e a tela do Windows sumir
        time.sleep(0.5)
    else:
        logger.warning("Não encontrou outras janelas do jogo no Windows+Tab. Apertando Esc para sair do Tab.")
        pyautogui.press('esc')
        time.sleep(0.5)
