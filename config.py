import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

_admins_raw = os.getenv("ADMIN_IDS", "").strip()
if _admins_raw:
    ADMIN_IDS = {int(x.strip()) for x in _admins_raw.split(",") if x.strip().isdigit()}
else:
    ADMIN_IDS = set()

ASSETS_WELCOME_PATH = os.path.join("assets", "welcome.png")
DATA_DIR = "data"
REG_CSV_PATH = os.path.join(DATA_DIR, "registrations.csv")
