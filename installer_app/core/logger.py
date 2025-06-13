import logging
import logging.config
from .config import load_config

config = load_config()
logging.config.dictConfig(config["logging"])
logger = logging.getLogger("installer-app")
