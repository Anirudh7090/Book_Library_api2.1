import logging
import os
import bcrypt
from datetime import datetime, timedelta

LOG_DIR = "../../logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "api.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message: str):
    print(message)  # Print to terminal console
    logging.info(message)  # Write to log file

def log_error(message: str):
    print(message)  # Print to terminal console
    logging.error(message)  # Write to log file

# Password hashing functions
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
