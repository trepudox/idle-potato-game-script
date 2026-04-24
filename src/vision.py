import cv2
import numpy as np
import mss
import easyocr
import os
import logging
from src.config import TEMPLATES_DIR, OPENCV_CONFIDENCE_THRESHOLD


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

def find_all_templates(template_name, img=None, threshold=OPENCV_CONFIDENCE_THRESHOLD, min_distance=10):
    """
    Busca todas as ocorrências de um template na tela.
    Retorna uma lista de tuplas com os centros (x, y) encontrados.
    Usa um limiar de distância para evitar detectar o mesmo botão várias vezes.
    """
    if img is None:
        img = capture_screen()

    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        logger.error(f"Template não encontrado: {template_path}")
        return []

    template = cv2.imread(template_path)
    h, w = template.shape[:2]
    
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    
    points = list(zip(*locations[::-1])) # Zipa para (x, y)
    
    if not points:
        return []
        
    # Filtra pontos muito próximos (simplificação de Non-Maximum Suppression)
    filtered_points = []
    for pt in points:
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        
        # Checa se já existe um ponto muito perto
        too_close = False
        for f_pt in filtered_points:
            dist = np.sqrt((center_x - f_pt[0])**2 + (center_y - f_pt[1])**2)
            if dist < min_distance:
                too_close = True
                break
        
        if not too_close:
            filtered_points.append((center_x, center_y))
            
    return filtered_points

def read_text_from_region(region, preprocess=False):
    """
    Captura uma região específica e lê o texto com EasyOCR.
    Region deve ser no formato {"top": y, "left": x, "width": w, "height": h}
    Se preprocess=True, aplica filtros de upscale e preto/branco.
    """
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        if preprocess:
            # Upscale 3x
            img_large = cv2.resize(img_bgr, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            # Tons de cinza
            gray = cv2.cvtColor(img_large, cv2.COLOR_BGR2GRAY)
            # Thresholding (B&W)
            _, processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        else:
            # EasyOCR prefere RGB
            processed_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # detail=0 retorna apenas a lista de strings
        result = reader.readtext(processed_img, detail=0)
        
        if result:
            text = " ".join(result)
            return text
        return ""
