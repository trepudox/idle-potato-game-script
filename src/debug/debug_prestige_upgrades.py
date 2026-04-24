import time
import cv2
import mss
import numpy as np
import pyautogui
from src import bot_actions
from src import vision
from src.config import PRESTIGE_UPGRADES_ANCHORS
from src.game_constants import TAB_BINDINGS, PRESTIGE
from src.utils import extract_number

print("=== INICIANDO DEBUG DE UPGRADES DE PRESTÍGIO ===")
print("Indo para a aba de Prestígio...")
bot_actions.press_key(TAB_BINDINGS[PRESTIGE])

print("Rolando a tela (-600 clicks) para encontrar os upgrades...")
bot_actions.scroll_down(clicks=-600, delay=1.0)
time.sleep(1)

with mss.mss() as sct:
    for upgrade_name, config_data in PRESTIGE_UPGRADES_ANCHORS.items():
        print(f"\n--- Procurando: {upgrade_name} ---")
        template_path = config_data["template"]
        
        loc = vision.find_template(template_path, threshold=0.8)
        if not loc:
            print(f"❌ Ícone do {upgrade_name} NÃO ENCONTRADO na tela!")
            continue
            
        x, y = loc
        print(f"✅ Ícone encontrado! Centro em X:{x}, Y:{y}")
        
        # Monta a região do OCR
        cost_region = {
            "top": int(y + config_data["cost_offset_y"]),
            "left": int(x + config_data["cost_offset_x"]),
            "width": config_data["cost_width"],
            "height": config_data["cost_height"]
        }
        
        # Tira um print dessa região exata para salvar a imagem
        sct_img = sct.grab(cost_region)
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Processamento idêntico ao vision.py
        img_large = cv2.resize(img_bgr, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img_large, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        filename = upgrade_name.lower().replace(" ", "_")
        cv2.imwrite(f"debug_{filename}_color.png", img_bgr)
        cv2.imwrite(f"debug_{filename}_bw.png", thresh)
        print(f"📸 Prints da caixinha salvos como debug_{filename}_color.png e _bw.png")
        
        # Lê o custo
        cost_text = vision.read_text_from_region(cost_region, preprocess=True)
        cost = extract_number(cost_text)
        print(f"👁️ OCR leu o texto bruto: '{cost_text}'")
        print(f"🔢 Valor final após limpar com Regex: {cost}")
        
        # Mover o mouse para o botão de comprar
        buy_x = int(x + config_data["buy_offset_x"])
        buy_y = int(y + config_data["buy_offset_y"])
        print(f"🖱️ Movendo o mouse para o botão de comprar em X:{buy_x}, Y:{buy_y}...")
        pyautogui.moveTo(buy_x, buy_y, duration=1.0)
        
        time.sleep(1.5)

print("\n=== DEBUG FINALIZADO ===")
print("Verifique as imagens geradas na pasta para confirmar se o enquadramento pegou todo o preço!")
# Sobe a tela de volta pra não bugar o jogo se for rodar de novo
bot_actions.scroll_up(clicks=500, delay=0.5)
