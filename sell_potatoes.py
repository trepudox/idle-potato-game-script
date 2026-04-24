from game_constants import *
from config import DEFAULT_ACTION_DELAY
import bot_actions
import vision
from config import SELL_POTATOES_REGIONS
from utils import extract_number
import logging


logger = logging.getLogger(__name__)


# Preços sem ponto flutante / 100 = 1.00
POTATOES_PRICE_THRESHOLD = 100
GOLDEN_POTATOES_PRICE_THRESHOLD = 6000


def try_sell_potatoes():
    bot_actions.press_key(TAB_BINDINGS[SELL_POTATOES])

    potatoes_sold = False
    golden_potatoes_sold = False

    potatoes_price_text = vision.read_text_from_region(SELL_POTATOES_REGIONS[POTATOES])[1:]
    golden_potatoes_price_text = vision.read_text_from_region(SELL_POTATOES_REGIONS[GOLDEN_POTATOES])[1:]

    logger.info(f"preco de batatas: {potatoes_price_text}")
    logger.info(f"preco de batatas douradas: {golden_potatoes_price_text}")

    potatoes_price = extract_number(potatoes_price_text)
    golden_potatoes_price = extract_number(golden_potatoes_price_text)

    logger.info(f"potatoes_price: {potatoes_price}")
    logger.info(f"golden_potatoes_price: {golden_potatoes_price}")

    if potatoes_price >= POTATOES_PRICE_THRESHOLD:
        logger.info("Vendendo batatas...")
        bot_actions.click_template('sell-potatoes/sell-all.png')
        potatoes_sold = True
        
    if golden_potatoes_price >= GOLDEN_POTATOES_PRICE_THRESHOLD:
        logger.info("Vendendo batatas douradas...")
        bot_actions.click_template('sell-potatoes/golden-potatoes.png')
        bot_actions.click_template('sell-potatoes/sell-all.png')
        golden_potatoes_sold = True

    return potatoes_sold, golden_potatoes_sold
