import os
import csv
from datetime import datetime
from typing import Optional, Dict, List

from config import REG_CSV_PATH, DATA_DIR

FIELDNAMES = ["telegram_id", "full_name", "phone", "region", "registered_at"]

def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(REG_CSV_PATH):
        with open(REG_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES)
            w.writeheader()

def _read_all() -> List[Dict[str, str]]:
    ensure_storage()
    with open(REG_CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def find_by_telegram_id(telegram_id: int) -> Optional[Dict[str, str]]:
    rows = _read_all()
    for r in rows:
        if str(telegram_id) == str(r.get("telegram_id", "")).strip():
            return r
    return None

def find_by_phone(phone: str) -> Optional[Dict[str, str]]:
    phone_norm = (phone or "").strip()
    rows = _read_all()
    for r in rows:
        if phone_norm == (r.get("phone", "") or "").strip():
            return r
    return None

def add_registration(telegram_id: int, full_name: str, phone: str, region: str) -> Dict[str, str]:
    ensure_storage()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = {
        "telegram_id": str(telegram_id),
        "full_name": full_name.strip(),
        "phone": phone.strip(),
        "region": region.strip(),
        "registered_at": now
    }

    if find_by_telegram_id(telegram_id) is not None:
        raise ValueError("already_registered_by_tg")
    if find_by_phone(phone) is not None:
        raise ValueError("phone_already_used")

    with open(REG_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writerow(row)

    return row