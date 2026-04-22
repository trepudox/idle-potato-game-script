import cv2
import numpy as np
import mss
import easyocr
import os
import logging
from config import TEMPLATES_DIR, OPENCV_CONFIDENCE_THRESHOLD


logger = logging.getLogger(__name__)


# Inicializa o leitor do EasyOCR
# Para usar GPU, configure gpu=True se tiver CUDA instalado
logger.info("Inicializando EasyOCR...")
reader = easyocr.Reader(['en'], gpu=False)

def capture_screen():
    """Captura a tela inteira usando mss e retorna a imagem no formato BGR para OpenCV."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Pega o monitor principal
        sct_img = sct.grab(monitor)
        
        # Converte a captura (BGRA) para BGR (formato padrão do OpenCV)
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img_bgr

def find_template(template_name, img=None, threshold=OPENCV_CONFIDENCE_THRESHOLD):
    """
    Busca uma imagem de template na tela e retorna as coordenadas do centro (x, y).
    Retorna None se não encontrar.
    """
    if img is None:
        img = capture_screen()

    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        logger.error(f"Template não encontrado: {template_path}")
        return None

    template = cv2.imread(template_path)
    
    # Faz o template matching
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # max_loc é o ponto superior esquerdo do match
        # Calcula o centro do template
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    
    return None

def read_text_from_region(region):
    """
    Captura uma região específica e lê o texto com EasyOCR.
    Region deve ser no formato {"top": y, "left": x, "width": w, "height": h}
    """
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # EasyOCR prefere RGB
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # detail=0 retorna apenas a lista de strings
        result = reader.readtext(img_rgb, detail=0)
        
        if result:
            text = " ".join(result)
            return text
        return ""
