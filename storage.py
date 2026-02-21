import os
import csv
import re
from datetime import datetime
from typing import Optional, Dict, List

from config import REG_CSV_PATH, DATA_DIR

# Янги формат
FIELDNAMES = ["telegram_id", "full_name", "phone", "region", "registered_at"]

# Эски формат (сенда ҳозир шу)
OLD_FIELDNAMES = ["fullname", "phone", "region", "created_at"]


def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(REG_CSV_PATH):
        with open(REG_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES)
            w.writeheader()


def _read_header() -> List[str]:
    if not os.path.exists(REG_CSV_PATH):
        return []
    with open(REG_CSV_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        return [h.strip() for h in header] if header else []


def normalize_phone(phone: str) -> str:
    # Фақат рақамлар: +998 93... -> 99893...
    return re.sub(r"\D+", "", phone or "").strip()


def migrate_old_csv_if_needed():
    """
    Агар registrations.csv эски форматда бўлса:
      fullname,phone,region,created_at
    уни автоматик янги форматга ўтказади ва эскисини .bak қилиб сақлайди.
    """
    if not os.path.exists(REG_CSV_PATH):
        return

    header = _read_header()
    if header == FIELDNAMES:
        return  # аллақачон янги

    if header != OLD_FIELDNAMES:
        # Номаълум формат — қўл тегизмаймиз
        return

    old_path = REG_CSV_PATH + ".bak"
    os.replace(REG_CSV_PATH, old_path)

    with open(old_path, "r", encoding="utf-8", newline="") as src, \
         open(REG_CSV_PATH, "w", encoding="utf-8", newline="") as dst:
        r = csv.DictReader(src)
        w = csv.DictWriter(dst, fieldnames=FIELDNAMES)
        w.writeheader()

        for row in r:
            w.writerow({
                "telegram_id": "",  # эски файлда tg_id йўқ
                "full_name": (row.get("fullname") or "").strip(),
                "phone": normalize_phone(row.get("phone") or ""),
                "region": (row.get("region") or "").strip(),
                "registered_at": (row.get("created_at") or "").strip(),
            })


def _read_all() -> List[Dict[str, str]]:
    ensure_storage()
    migrate_old_csv_if_needed()
    with open(REG_CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def find_by_telegram_id(telegram_id: int) -> Optional[Dict[str, str]]:
    tid = str(telegram_id).strip()
    for r in _read_all():
        if tid == str(r.get("telegram_id", "")).strip():
            return r
    return None


def find_by_phone(phone: str) -> Optional[Dict[str, str]]:
    p = normalize_phone(phone)
    for r in _read_all():
        if p and p == normalize_phone(r.get("phone", "") or ""):
            return r
    return None


def add_registration(telegram_id: int, full_name: str, phone: str, region: str) -> Dict[str, str]:
    ensure_storage()
    migrate_old_csv_if_needed()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tid = str(telegram_id).strip()
    phone_norm = normalize_phone(phone)

    rows = _read_all()
    for r in rows:
        if tid == str(r.get("telegram_id", "")).strip():
            raise ValueError("already_registered_by_tg")
        if phone_norm and phone_norm == normalize_phone(r.get("phone", "") or ""):
            raise ValueError("phone_already_used")

    row = {
        "telegram_id": tid,
        "full_name": (full_name or "").strip(),
        "phone": phone_norm,
        "region": (region or "").strip(),
        "registered_at": now
    }

    with open(REG_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writerow(row)

    return row


def bind_telegram_id_by_phone(telegram_id: int, phone: str) -> bool:
    """
    Миграциядан кейин telegram_id бўш қолади.
    Агар user телефон юборса ва шу телефон CSVда бор бўлса,
    ўша қаторга telegram_id ни боғлаб қўямиз.
    """
    ensure_storage()
    migrate_old_csv_if_needed()

    tid = str(telegram_id).strip()
    phone_norm = normalize_phone(phone)
    if not phone_norm:
        return False

    rows = _read_all()
    changed = False

    for r in rows:
        if phone_norm == normalize_phone(r.get("phone", "") or ""):
            if not str(r.get("telegram_id", "")).strip():
                r["telegram_id"] = tid
                changed = True
            break

    if not changed:
        return False

    with open(REG_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for r in rows:
            w.writerow({
                "telegram_id": str(r.get("telegram_id", "")).strip(),
                "full_name": (r.get("full_name") or "").strip(),
                "phone": normalize_phone(r.get("phone") or ""),
                "region": (r.get("region") or "").strip(),
                "registered_at": (r.get("registered_at") or "").strip(),
            })

    return True


def list_last(limit: int = 20) -> List[Dict[str, str]]:
    rows = _read_all()
    rows = [r for r in rows if any((v or "").strip() for v in r.values())]
    return rows[-limit:]