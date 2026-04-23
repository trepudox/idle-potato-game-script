from game_constants import MULTIPLIERS
import logging

logger = logging.getLogger(__name__)


def extract_number(text):
    """Função utilitária para limpar o texto lido pelo OCR e converter para inteiro com multiplicadores"""
    text = text.replace(" ", "").strip()
    if not text:
        return -1
        
    for suffix, multiplier in MULTIPLIERS.items():
        if text.lower().endswith(suffix.lower()):
            number_part = text[:-len(suffix)]
            number_part = number_part.replace(',', '.')
            # Remove qualquer caracter inválido da parte numérica (ex: erros pequenos do OCR)
            clean_num = ''.join(c for c in number_part if c.isdigit() or c == '.')
            if clean_num:
                try:
                    return int(float(clean_num) * multiplier)
                except ValueError as e:
                    logger.warning(f"Erro ao converter número: {e}")
                    pass
            break
            
    # Fallback se não tiver sufixo
    clean_text = ''.join(filter(str.isdigit, text))
    if clean_text:
        return int(clean_text)

    return -1
