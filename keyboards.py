from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

CTA_JOIN_TEXT = "👉 Ishtirok etmoqchiman"
BTN_MY_INFO = "📄 Ma’lumotlarim"
BTN_HELP = "ℹ️ Yordam"

def kb_welcome():
    return ReplyKeyboardMarkup(
        [[KeyboardButton(CTA_JOIN_TEXT)]],
        resize_keyboard=True
    )

def kb_after_registered():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_MY_INFO)],
            [KeyboardButton(BTN_HELP)]
        ],
        resize_keyboard=True
    )

def kb_contact_share():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📞 Telefon raqamimni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

REGIONS = [
    "Toshkent viloyati",
    "Toshkent shahri",
    "Samarqand",
    "Andijon",
    "Farg‘ona",
    "Namangan",
    "Buxoro",
    "Xorazm",
    "Qashqadaryo",
    "Surxondaryo",
    "Jizzax",
    "Sirdaryo",
    "Navoiy",
    "Qoraqalpog‘iston Respublikasi",
]

def kb_regions():
    rows = []
    row = []
    for r in REGIONS:
        row.append(KeyboardButton(r))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    return ReplyKeyboardMarkup(rows, resize_keyboard=True, one_time_keyboard=True)

def kb_remove():
    return ReplyKeyboardRemove()