from game_constants import MULTIPLIERS
import logging

logger = logging.getLogger(__name__)


import re

def extract_number(text):
    """
    Limpa o texto lido pelo OCR e converte para inteiro com multiplicadores.
    Se houver vários números (ex: preço riscado 'Cost 720 360'), pega sempre o último.
    """
    if not text:
        return -1
        
    # Encontra todos os blocos numéricos (com ou sem sufixo de letra)
    # Ex: 'Cost: 720 360Qa' vira ['720 ', '360Qa']
    matches = re.findall(r'[\d\.,]+\s*[a-zA-Z]*', text)
    
    if not matches:
        # Hack de OCR: o EasyOCR costuma engolir o número "1" porque ele é muito fino (ex: 'Cost PP').
        # Como no jogo, se apareceu Cost e PP mas não tem número, 99% de chance de ser 1!
        if "cost" in text.lower() and "pp" in text.lower():
            return 1
        return -1
        
    # Analisa do último para o primeiro até achar um número válido
    for match in reversed(matches):
        match = match.replace(" ", "").strip()
        
        for suffix, multiplier in MULTIPLIERS.items():
            if match.lower().endswith(suffix.lower()):
                number_part = match[:-len(suffix)]
                number_part = number_part.replace(',', '.')
                clean_num = ''.join(c for c in number_part if c.isdigit() or c == '.')
                if clean_num:
                    try:
                        return int(float(clean_num) * multiplier)
                    except ValueError as e:
                        logger.warning(f"Erro ao converter número: {e}")
                        pass
                break # Para não testar outros sufixos se já deu match no final
                
        # Fallback se não tiver sufixo (ex: '360')
        clean_text = ''.join(filter(str.isdigit, match))
        if clean_text:
            return int(clean_text)

    return -1
