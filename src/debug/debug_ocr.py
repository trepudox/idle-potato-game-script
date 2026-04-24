

from src import bot_actions
from src import vision
from src.config import RESOURCES_REGIONS
from src.game_constants import POTENTIAL_PP
import cv2
import mss
import numpy as np

region = RESOURCES_REGIONS[POTENTIAL_PP]
print(f"Lendo região do POTENTIAL_PP: {region}")

with mss.mss() as sct:
    sct_img = sct.grab(region)
    img = np.array(sct_img)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    
    cv2.imwrite("debug_pp.png", img_bgr)
    print("Imagem original salva como 'debug_pp.png'.")
    
    # --- PRÉ-PROCESSAMENTO (Preto e Branco / Aumento de Escala) ---
    img_large = cv2.resize(img_bgr, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img_large, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    cv2.imwrite("debug_pp_bw.png", thresh)
    print("Imagem tratada salva como 'debug_pp_bw.png'. Abra ela e veja se ficou legível!")

# O vision.py já possui o preprocess=True configurado, vamos usar ele direto
text = vision.read_text_from_region(region, preprocess=True)
print(f"O EasyOCR leu: '{text}'")
