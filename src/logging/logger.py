import logging
import sys, os
from datetime import datetime

LOG_FORMAT = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(), "logs")
LOG_PATH = os.path.join(log_path, LOG_FORMAT)
os.makedirs(log_path, exist_ok=True)
logging.basicConfig(filename=LOG_PATH,
    level=logging.INFO,
    format="[ %(asctime)s ] - %(lineno)d - %(levelname)s - %(message)s",
)