import time
from src.game_constants import *
from src.config import RESOURCES_REGIONS
from src import vision
from src.utils import extract_number
import cv2
import mss
import numpy as np

print("="*50)
print("--- DEBUG DE LEITURA DE RECURSOS ---")
print("="*50)

print("\n[1/2] Salvando recortes da tela para auditoria visual...")
with mss.mss() as sct:
    for res_name, region in RESOURCES_REGIONS.items():
        if res_name == ASCENSION_COST:
            continue # O custo de ascensão não fica na aba Home
            
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        filename = f"debug_resource_{res_name.replace(' ', '_').lower()}.png"
        cv2.imwrite(filename, img_bgr)
        print(f" -> Imagem salva: {filename}")

print("\n[2/2] Testando motor do EasyOCR e Regex de conversão...")

# Faz a leitura do OCR como se estivesse no app.py
potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[POTATOES])
golden_potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[GOLDEN_POTATOES])
magic_potatoes_text = vision.read_text_from_region(RESOURCES_REGIONS[MAGIC_POTATOES])

# Cash tem a malandragem do primeiro caractere (o símbolo $)
raw_cash_text = vision.read_text_from_region(RESOURCES_REGIONS[CASH])
cash_text = raw_cash_text[1:] if raw_cash_text else ""

# PPs usam pré-processamento (Upscale + B&W)
current_pp_text = vision.read_text_from_region(RESOURCES_REGIONS[CURRENT_PP], preprocess=True)
potential_pp_text = vision.read_text_from_region(RESOURCES_REGIONS[POTENTIAL_PP], preprocess=True)

print("\n--- RESULTADOS FINAIS ---")
print(f"{'RECURSO':<20} | {'TEXTO CRU (OCR)':<20} | {'VALOR NUMÉRICO EXTRAÍDO'}")
print("-" * 70)
print(f"{POTATOES:<20} | '{potatoes_text:<18}' | {extract_number(potatoes_text)}")
print(f"{GOLDEN_POTATOES:<20} | '{golden_potatoes_text:<18}' | {extract_number(golden_potatoes_text)}")
print(f"{MAGIC_POTATOES:<20} | '{magic_potatoes_text:<18}' | {extract_number(magic_potatoes_text)}")
print(f"{CASH:<20} | '{raw_cash_text:<18}' | {extract_number(cash_text)} (usou slice [1:])")
print(f"{CURRENT_PP:<20} | '{current_pp_text:<18}' | {extract_number(current_pp_text)}")
print(f"{POTENTIAL_PP:<20} | '{potential_pp_text:<18}' | {extract_number(potential_pp_text)}")

print("\nPronto! Analise as imagens salvas na pasta para garantir que o crop está perfeito.")
