import os
import sys
from typing import Final

from loguru import logger

from .bot import query_bot_rates
from .dbs import query_dbs_rates
from .esun import query_esun_rates
from .sinopac import query_sinopac_rates
from .types import Exchange
from .types import Rate

LOGURU_LEVEL: Final[str] = os.getenv("LOGURU_LEVEL", "INFO")
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGURU_LEVEL}])
