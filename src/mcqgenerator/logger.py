# logging info, tracking changes etc 

import logging
import os
from datetime import datetime
logging.info("Logger test - it works!")


LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)
log_filepath = os.path.join(log_path, LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    filename=log_filepath,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
