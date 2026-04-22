from config import DEFAULT_ACTION_DELAY
import time
import bot_actions
from constants import *
import vision
from config import SELL_POTATOES_REGIONS
from utils import extract_number
import logging


logger = logging.getLogger(__name__)


POTATOES_PRICE_THRESHOLD = 1
# POTATOES_PRICE_THRESHOLD = 100
GOLDEN_POTATOES_PRICE_THRESHOLD = 6
# GOLDEN_POTATOES_PRICE_THRESHOLD = 6000

def try_sell_potatoes():
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
        
    if golden_potatoes_price >= GOLDEN_POTATOES_PRICE_THRESHOLD:
        logger.info("Vendendo batatas douradas...")
        bot_actions.click_template('sell-potatoes/golden-potatoes.png')
        time.sleep(DEFAULT_ACTION_DELAY)
        bot_actions.click_template('sell-potatoes/sell-all.png')
