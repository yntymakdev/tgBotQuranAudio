# 📦 Установи перед запуском:
# pip install python-telegram-bot==13.15 requests
import re
import os
import requests
from dotenv import load_dotenv
from telegram.ext import MessageHandler, Filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from difflib import get_close_matches  # для поиска похожих
load_dotenv()
# === Настройки ===
TOKEN = os.getenv("TOKEN_TG")
API_BASE = "https://api.alquran.cloud/v1"
LANGUAGE_CODE = "ru.kuliev"  # Можно заменить на ky.osmonov если появится поддержка


# === Получение списка сур ===
def get_surahs():
    try:
        response = requests.get(f"{API_BASE}/surah")
        return response.json()["data"]
    except:
        return []
SURA_OFFICIAL_NAMES = {
    1: "Аль-Фатиха",
    2: "Аль-Бакара",
    3: "Аль-Имран",
    4: "Ан-Ниса",
    5: "Аль-Маида",
    6: "Аль-Ан'ам",
    7: "Аль-А'раф",
    8: "Аль-Анфаль",
    9: "Ат-Тауба",
    10: "Юнус",
    11: "Худ",
    12: "Юсуф",
    13: "Ар-Ра'д",
    14: "Ибрахим",
    15: "Аль-Хиджр",
    16: "Ан-Нахль",
    17: "Аль-Исра",
    18: "Аль-Кахф",
    19: "Мариям",
    20: "Та-Ха",
    21: "Аль-Анбия",
    22: "Аль-Хадж",
    23: "Аль-Му'минун",
    24: "Ан-Нур",
    25: "Аль-Фуркан",
    26: "Аш-Шуара",
    27: "Ан-Намль",
    28: "Аль-Касас",
    29: "Аль-Анкабут",
    30: "Ар-Рум",
    31: "Лукман",
    32: "Ас-Саджда",
    33: "Аль-Ахзаб",
    34: "Саба",
    35: "Фатир",
    36: "Ясин",
    37: "Ас-Саффат",
    38: "Сад",
    39: "Аз-Зумар",
    40: "Гафир",
    41: "Фуссилат",
    42: "Аш-Шура",
    43: "Аз-Зухруф",
    44: "Ад-Духан",
    45: "Аль-Джасия",
    46: "Аль-Ахкаф",
    47: "Мухаммад",
    48: "Аль-Фатх",
    49: "Аль-Худжурат",
    50: "Каф",
    51: "Аз-Зарият",
    52: "Ат-Тур",
    53: "Ан-Наджм",
    54: "Аль-Камар",
    55: "Ар-Рахман",
    56: "Аль-Вакиа",
    57: "Аль-Хадид",
    58: "Аль-Муджадила",
    59: "Аль-Хашр",
    60: "Аль-Мумтахина",
    61: "Ас-Сафф",
    62: "Аль-Джуму'а",
    63: "Аль-Мунафикун",
    64: "Ат-Тагабун",
    65: "Ат-Талак",
    66: "Ат-Тахрим",
    67: "Аль-Мульк",
    68: "Аль-Калям",
    69: "Аль-Хакка",
    70: "Аль-Ма'аридж",
    71: "Нух",
    72: "Аль-Джинн",
    73: "Аль-Муззаммиль",
    74: "Аль-Муддассир",
    75: "Аль-Кийама",
    76: "Аль-Инсан",
    77: "Аль-Мурсалят",
    78: "Ан-Наба",
    79: "Ан-Назиат",
    80: "Абаса",
    81: "Ат-Таквир",
    82: "Аль-Инфитар",
    83: "Аль-Мутаффифин",
    84: "Аль-Иншикак",
    85: "Аль-Бурудж",
    86: "Ат-Тарик",
    87: "Аль-А'ля",
    88: "Аль-Гашия",
    89: "Аль-Фаджр",
    90: "Аль-Балад",
    91: "Аш-Шамс",
    92: "Аль-Лайл",
    93: "Ад-Духа",
    94: "Аш-Шарх",
    95: "Ат-Тин",
    96: "Аль-Аляк",
    97: "Аль-Кадр",
    98: "Аль-Баййина",
    99: "Аз-Залзала",
    100: "Аль-Адият",
    101: "Аль-Кариа",
    102: "Ат-Такасур",
    103: "Аль-Аср",
    104: "Аль-Хумаза",
    105: "Аль-Филь",
    106: "Курайш",
    107: "Аль-Ма'ун",
    108: "Аль-Каусар",
    109: "Аль-Кафирун",
    110: "Ан-Наср",
    111: "Аль-Масад",
    112: "Аль-Ихляс",
    113: "Аль-Фаляк",
    114: "Ан-Нас"
}

RUSSIAN_SURA_NAMES = {
    "фатиха": 1, "алфатиха": 1, "альфатиха": 1,
    "бакара": 2, "альбакара": 2,
    "имран": 3, "альимран": 3,
    "анниса": 4, "альанниса": 4,
    "маида": 5, "альмаида": 5,
    "анам": 6, "альанам": 6,
    "араф": 7, "альараф": 7,
    "анфал": 8, "альанфал": 8,
    "аттауаба": 9, "аттауба": 9, "аттавба": 9, "альаттауаба": 9,
    "юнус": 10, "юнуc": 10,
    "худ": 11, "альхуд": 11,
    "юсуф": 12, "альюсуф": 12,
    "аррад": 13, "альаррад": 13,
    "ибрахим": 14, "альибрахим": 14,
    "хиджр": 15, "альхиджр": 15,
    "аннахль": 16, "нахль": 16,
    "исра": 17, "альисра": 17,
    "кахф": 18, "алькахф": 18,
    "мариям": 19, "альмариям": 19,
    "Та Ха": 20, "таха": 20,
    "анбийа": 21, "альанбийа": 21,
    "хадж": 22, "альхадж": 22,
    "муминун": 23, "альмуминун": 23,
    "нур": 24, "аннур": 24,
    "фуркан": 25, "альфуркан": 25,
    "шуара": 26, "альшуара": 26,
    "анамл": 27, "альанамл": 27,
    "касас": 28, "алькасас": 28,
    "анкабут": 29, "альанкабут": 29,
    "рум": 30, "альрум": 30,
    "лукман": 31, "альлукман": 31,
    "садждах": 32, "альсадждах": 32,
    "ахзаб": 33, "альахзаб": 33,
    "саба": 34, "альсаба": 34,
    "фаджр": 35, "ясин": 36, "ассаффат": 37,
    "саджда": 38, "аззумар": 39,
    "гафир": 40, "фуссилат": 41,
    "ашшура": 42, "аззухруф": 43,
    "аддухан": 44, "альджатия": 45,
    "алахкаф": 46, "мухаммад": 47,
    "альфатх": 48, "альхуджурат": 49,
    "гаф": 50, "аззарият": 51,
    "аттур": 52, "аннаджм": 53,
    "алькамар": 54, "аррахман": 55,
    "альвакия": 56, "альхадид": 57,
    "альмуджадиля": 58, "альхашр": 59,
    "альмутахана": 60,
    "ассафф": 61, "альджумуа": 62,
    "альмунафикун": 63, "аттагабун": 64,
    "атталяк": 65,
    "аттахрим": 66, "альмулк": 67,
    "алькалам": 68, "альхакка": 69,
    "альмааридж": 70, "нух": 71,
    "альджинн": 72, "альмуззаллим": 73,
    "альмуддасир": 74, "алькияма": 75,
    "альмурсалят": 77, "аннаба": 78,
    "анназиат": 79, "абасса": 80,
    "аттаквир": 81, "альинфитар": 82,
    "альмутаффивин": 83, "альиншикак": 84,
    "альбурудж": 85, "аттарик": 86,
    "альала": 87, "альгашия": 88,
    "альфаджр": 89, "альбаляд": 90,
    "ашшамс": 91, "альляйль": 92,
    "аддуха": 93, "ашшарх": 94,
    "аттин": 95, "альаляк": 96,
    "алькадр": 97, "альбаййина": 98,
    "аззальзаля": 99, "альадият": 100,
    "алькариа": 101, "аттакасур": 102,
    "альаср": 103, "альхумаза": 104,
    "альфиль": 105, "курайш": 106,
    "альмаун": 107, "алькавсар": 108,
    "алькафирун": 109,
    "аннаср": 110, "альмасад": 111,
    "альихляс": 112, "альфаляк": 113,
    "аннас": 114
}

def welcome_fallback(update: Update, context: CallbackContext):
    text = (
        "🕌 *Ассаламу алейкум!*\n"
        "Добро пожаловать в *Quran Audio Bot*! 📖✨\n\n"
        "🎯 *Что умеет этот бот:*\n"
        "• 🎧 Слушай аяты Корана\n"
        "• 📚 Читай переводы\n"
        "• 🔍 Ищи по словам или номерам\n\n"
        "🧠 *Как искать аят:*\n"
        "Напиши, например:\n"
        "• \\`Сура Аль\\-Бакара аят 255\\`\n"
        "• \\`2:255\\`\n"
        "• \\`36\\-58\\`\n\n"
        "И получишь нужный аят, перевод и аудио! 🎧\n\n"
        "🚀 *Выберите действие ниже:*"
    )

    update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN_V2
    )

# === Получение аятов и перевода ===
def get_surah_ayahs(surah_number):
    try:
        ar_resp = requests.get(f"{API_BASE}/surah/{surah_number}/ar.alafasy").json()
        tr_resp = requests.get(f"{API_BASE}/surah/{surah_number}/{LANGUAGE_CODE}").json()
        return ar_resp["data"]["ayahs"], tr_resp["data"]["ayahs"]
    except:
        return [], []
def handle_text_ayah_request(update, context):
        text = update.message.text.lower().strip()

        # Формат: 10:3 или 10-3
        colon_match = re.match(r"(\d{1,3})[:\-](\d+)", text)

        if colon_match:
            surah_num = int(colon_match.group(1))
            ayah_num = int(colon_match.group(2))

            _, tr_ayahs = get_surah_ayahs(surah_num)
            total_ayahs = len(tr_ayahs)

            if ayah_num <= 0 or ayah_num > total_ayahs:
                update.message.reply_text(f"❌ В суре {surah_num} нет аята {ayah_num}.")
                return

            ayah_data = get_ayah(surah_num, ayah_num)
            if not ayah_data or not isinstance(ayah_data, dict):
                update.message.reply_text("❌ Ошибка при получении аята.")
                return

            translation = tr_ayahs[ayah_num - 1]['text'] if ayah_num <= total_ayahs else ""

            update.message.reply_text(
                f"📖 *Сура {surah_num}, Аят {ayah_num}*\n\n"
                f"🗌 {ayah_data['text']}\n\n"
                f"📘 Перевод: _{translation}_",
                parse_mode=ParseMode.MARKDOWN
            )
            update.message.reply_audio(
                audio=ayah_data["audio"],
                title=f"Сура {surah_num}, Аят {ayah_num}"
            )
            return

        # Формат: Сура Аль-Бакара аят 8
        match = re.search(r"сура ([а-яёa-z\- ]+) аят (\d+)", text)
        if match:
            sura_name = match.group(1).strip().replace("аль", "").replace(" ", "")
            ayah_num = int(match.group(2))

            surah_num = RUSSIAN_SURA_NAMES.get(sura_name)
            if not surah_num:
                update.message.reply_text("❌ Сура не найдена. Попробуйте написать точнее.")
                return

            _, tr_ayahs = get_surah_ayahs(surah_num)

            if ayah_num <= 0 or ayah_num > len(tr_ayahs):
                update.message.reply_text(
                    f"❌ В суре №{surah_num} нет аята под номером {ayah_num}."
                )
                return

            ayah_data = get_ayah(surah_num, ayah_num)
            if not ayah_data:
                update.message.reply_text("❌ Аят не найден.")
                return

            translation = tr_ayahs[ayah_num - 1]['text']

            update.message.reply_text(
                f"📖 *Сура {surah_num}, Аят {ayah_num}*\n\n"
                f"🗌 {ayah_data['text']}\n\n"
                f"📘 Перевод: _{translation}_",
                parse_mode=ParseMode.MARKDOWN
            )
            update.message.reply_audio(
                audio=ayah_data["audio"],
                title=f"Сура {surah_num}, Аят {ayah_num}"
            )
            return

        update.message.reply_text("🔍 Введите запрос в формате:  `2:255`", parse_mode=ParseMode.MARKDOWN)


# === Получение одного аята ===
def get_ayah(surah, ayah):
    try:
        resp = requests.get(f"{API_BASE}/ayah/{surah}:{ayah}/ar.alafasy").json()
        if resp.get("status") == "OK":
            return resp["data"]
        else:
            return None
    except:
        return None


# === Команда /start ===
def start(update: Update, context: CallbackContext):
    welcome_text = (
    "🕌 *Ассаламу алейкум!*\n"
    "Добро пожаловать в *Quran Audio Bot*! 📖✨\n\n"
    "🎯 *Что умеет этот бот:*\n"
    "• 🎧 Слушай аяты Корана\n"
    "• 📚 Читай переводы\n"
    "• 🔍 Ищи по названием или номерам\n\n"
    "🧠 *Как искать аят:*\n"
    "Напиши, например:\n"
    "• \\`2:255\\`\n"
    "И получишь нужный аят, перевод и аудио! 🎧\n\n"
    "🚀 *Выберите действие ниже:*"
    )

    keyboard = [
        [InlineKeyboardButton("📖 Выбрать суру", callback_data="show_surahs_0")],
        [InlineKeyboardButton("🔍 Поиск", callback_data="search_help")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]

    update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Главное меню ===
def show_main_menu(query):
    welcome_text = (
        "🕌 *Главное меню*\n\n"
        "🎯 *Выберите действие:*"
    )

    keyboard = [
        [InlineKeyboardButton("📖 Выбрать суру", callback_data="show_surahs_0")],
        [InlineKeyboardButton("🔍 Поиск", callback_data="search_help")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]

    query.edit_message_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Команда /menu ===
def menu(update: Update, context: CallbackContext):
    welcome_text = (
        "🕌 *Главное меню*\n\n"
        "🎯 *Выберите действие:*"
    )

    keyboard = [
        [InlineKeyboardButton("📖 Выбрать суру", callback_data="show_surahs_0")],
        [InlineKeyboardButton("🔍 Поиск", callback_data="search_help")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]

    update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Команда /help ===
def help_command(update: Update, context: CallbackContext):
    help_text = (
        "📋 *Подробная инструкция:*\n\n"
        "🚀 *Основные команды:*\n"
        "• /start - запуск бота\n"
        "• /menu - главное меню\n"
        "• /help - эта справка\n"
        "• /search [слово] - поиск по названию\n\n"
        "📖 *Как пользоваться:*\n"
        "1️⃣ Выберите суру из списка\n"
        "2️⃣ Выберите нужный аят\n"
        "3️⃣ Получите аудио и перевод\n"
        "4️⃣ Используйте кнопки для навигации\n\n"
        "🔍 *Поиск:*\n"
        "Введите /search и слово для поиска\n"
        "Пример: /search Аль Фатиха\n\n"
        "💡 *Совет:* Используйте кнопки для удобной навигации!"
    )

    keyboard = [
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]

    update.message.reply_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Помощь по поиску ===
def show_search_help(query):
    help_text = (
        "🔍 *Как использовать поиск:*\n\n"
        "📝 *Способы поиска:*\n"
        "• Используйте команду: /search [слово]\n"
        "• Пример: /search Аль Фатиха\n"
        "⚡ *Быстрый поиск:*\n"
        "Нажмите кнопку ниже и введите слово для поиска"
    )

    keyboard = [
        [InlineKeyboardButton("🔍 Начать поиск", callback_data="start_search")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]

    query.edit_message_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Вывод страницы с сурами ===
def show_surah_page(query, page):
    surahs = get_surahs()
    if not surahs:
        query.edit_message_text("❌ Ошибка загрузки сур. Попробуйте позже.")
        return

    page_size = 15
    start_idx = page * page_size
    end_idx = start_idx + page_size

    text = f"📚 *Список сур Корана* (стр. {page + 1})\n\n"
    keyboard = []

    for s in surahs[start_idx:end_idx]:
        # Красивое оформление кнопок сур
        btn_text = f"📖 {s['number']}. {s['englishName']}"
        if len(btn_text) > 30:
            btn_text = btn_text[:27] + "..."

        btn = InlineKeyboardButton(btn_text, callback_data=f"surah_{s['number']}")
        keyboard.append([btn])

    # Навигация
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"show_surahs_{page - 1}"))
    if end_idx < len(surahs):
        nav_buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"show_surahs_{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    # Кнопка в главное меню
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])

    query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Показ аятов суры ===
def show_surah_ayahs(query, surah_num, page=0):
    ar_ayahs, tr_ayahs = get_surah_ayahs(surah_num)

    if not ar_ayahs:
        query.edit_message_text("❌ Ошибка загрузки аятов. Попробуйте позже.")
        return

    surahs = get_surahs()
    surah_name = next((s['englishName'] for s in surahs if s['number'] == surah_num), f"Сура {surah_num}")

    page_size = 15
    start_idx = page * page_size
    end_idx = start_idx + page_size

    text = f"📖 *{surah_name}*\n"
    text += f"📊 Всего аятов: {len(ar_ayahs)}\n\n"
    text += f"🔹 *Выберите аят:*"

    keyboard = []

    for i, ayah in enumerate(ar_ayahs[start_idx:end_idx], start=start_idx + 1):
        btn_text = f"🔹 Аят {i}"
        btn = InlineKeyboardButton(btn_text, callback_data=f"ayah_{surah_num}_{i}")
        keyboard.append([btn])

    # Навигация по аятам
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"surah_page_{surah_num}_{page - 1}"))
    if end_idx < len(ar_ayahs):
        nav_buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"surah_page_{surah_num}_{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    # Кнопки навигации
    keyboard.append([
        InlineKeyboardButton("📚 К сурам", callback_data="show_surahs_0"),
        InlineKeyboardButton("📝 Читать всю суру", callback_data=f"surah_full_{surah_num}_0"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")

    ])

    query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Показ аята ===
def show_ayah(query, surah_num, ayah_num):
    ayah_data = get_ayah(surah_num, ayah_num)

    if not ayah_data:
        query.answer("❌ Ошибка загрузки аята")
        return

    # Получаем перевод
    _, tr_ayahs = get_surah_ayahs(surah_num)
    translation = ""
    if tr_ayahs and len(tr_ayahs) >= ayah_num:
        translation = tr_ayahs[ayah_num - 1]["text"]

    # Получаем информацию о суре
    surahs = get_surahs()
    surah_name = next((s['englishName'] for s in surahs if s['number'] == surah_num), f"Сура {surah_num}")

    # Текст сообщения
    text = f"📖 *{surah_name}*\n"
    text += f"🔹 *Аят {ayah_num}*\n\n"
    text += f"📝 *Перевод:*\n_{translation}_\n\n"
    text += f"🎧 *Аудио отправляется...*"

    # Кнопки навигации
    keyboard = [
        [InlineKeyboardButton("↩️ К аятам суры", callback_data=f"surah_{surah_num}")],
        [InlineKeyboardButton("📚 К сурам", callback_data="show_surahs_0")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]

    # Отправляем аудио
    try:
        query.message.reply_audio(
            audio=ayah_data["audio"],
            title=f"Аят {ayah_num} - {surah_name}",
            caption=f"🎧 *Аят {ayah_num}* из суры *{surah_name}*",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Ошибка отправки аудио: {e}")

    # Отправляем текст с переводом
    query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
    # Отправить аудио всей суры автоматически
    bitrate = 128
    edition = "ar.alafasy"
    surah_str = str(surah_num)
    audio_url = f"https://cdn.islamic.network/quran/audio-surah/{bitrate}/{edition}/{surah_str}.mp3"

    surahs = get_surahs()
    surah_name = next((s['englishName'] for s in surahs if s['number'] == surah_num), f"Сура {surah_num}")

    try:
        query.message.reply_audio(
            audio=audio_url,
            title=f"Сура {surah_name}",
            caption=f"🎧 Аудио полной суры *{surah_name}*",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Ошибка отправки аудио полной суры: {e}")


# === Обработка кнопок ===
def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    try:
        if data == "main_menu":
            show_main_menu(query)

        elif data == "help":
            help_text = (
                "📋 *Подробная инструкция:*\n\n"
                "🚀 *Основные команды:*\n"
                "• /start - запуск бота\n"
                "• /menu - главное меню\n"
                "• /help - эта справка\n"
                "• /search [слово] - поиск по переводу\n\n"
                "📖 *Как пользоваться:*\n"
                "1️⃣ Выберите суру из списка\n"
                "2️⃣ Выберите нужный аят\n"
                "3️⃣ Получите аудио и перевод\n"
                "4️⃣ Используйте кнопки для навигации\n\n"
                "🔍 *Поиск:*\n"
                "Введите /search и слово для поиска\n"
                "Пример: /search милость\n\n"
                "💡 *Совет:* Используйте кнопки для удобной навигации!"
            )

            keyboard = [
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]

            query.edit_message_text(
                help_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )

        elif data == "search_help":
            show_search_help(query)

        elif data == "start_search":
            query.edit_message_text(
                "🔍 *Поиск по Корану*\n\n"
                "📝 Введите команду и слово для поиска:\n"
                "`/search [ваше слово]`\n\n"
                "💡 *Пример:* /search милость",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
                ]),
                parse_mode=ParseMode.MARKDOWN
            )

        elif data.startswith("show_surahs_"):
            page = int(data.split("_")[2])
            show_surah_page(query, page)

        elif data.startswith("surah_page_"):
            parts = data.split("_")
            surah_num = int(parts[2])
            page = int(parts[3])
            show_surah_ayahs(query, surah_num, page)
        elif data.startswith("surah_full_"):
            parts = data.split("_")
            surah_num = int(parts[2])
            page = int(parts[3])
            show_full_surah_page(update.callback_query, surah_num, page)

        elif data.startswith("surah_"):
            surah_num = int(data.split("_")[1])
            show_surah_ayahs(query, surah_num)

        elif data.startswith("ayah_"):
            parts = data.split("_")
            surah_num = int(parts[1])
            ayah_num = int(parts[2])
            show_ayah(query, surah_num, ayah_num)

    except Exception as e:
        print(f"Ошибка обработки кнопки: {e}")
        query.edit_message_text(
            "❌ Произошла ошибка. Попробуйте снова.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ])
        )

def normalize(text):
    text = text.lower()
    text = re.sub(r"[ьъ\-]", "", text)
    text = text.replace("аль", "")
    text = re.sub(r"\s+", "", text)
    return text
# === Поиск по переводу ===
def search(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text(
            "🔍 Введите название суры после команды /search",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    input_text = ' '.join(context.args)
    normalized_input = normalize(input_text)

    # Ищем все совпадения по подстроке
    matches = [(name, num) for name, num in RUSSIAN_SURA_NAMES.items() if normalized_input in name]

    # Удаляем повторы по номеру суры (чтобы не было 3х "Аль-Фатиха")
    unique_matches = {}
    for name, num in matches:
        if num not in unique_matches:
            unique_matches[num] = name

    if unique_matches:
        text = f"🔍 Найдено {len(unique_matches)} совпадений для \"{input_text}\":\n\n"
        keyboard = []
        for num, name in list(unique_matches.items())[:10]:
            official_name = SURA_OFFICIAL_NAMES.get(num, name.title())
            text += f"• {official_name}\n"
            keyboard.append([InlineKeyboardButton(official_name, callback_data=f"surah_{num}")])

        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])

        update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Если совпадений нет — ищем похожие названия (подсказки)
    close_matches = get_close_matches(normalized_input, RUSSIAN_SURA_NAMES.keys(), n=5, cutoff=0.5)

    if close_matches:
        text = f"🔍 Точных совпадений не найдено. Возможно, вы имели в виду:\n\n"
        keyboard = []
        shown = set()
        for name in close_matches:
            num = RUSSIAN_SURA_NAMES[name]
            if num in shown:
                continue  # пропустить повтор
            shown.add(num)
            official_name = SURA_OFFICIAL_NAMES.get(num, name.title())
            text += f"• {official_name}\n"
            keyboard.append([InlineKeyboardButton(official_name, callback_data=f"surah_{num}")])

        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])

        update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_text(
            f"❌ По запросу \"{input_text}\" ничего не найдено и похожих вариантов нет.",
            parse_mode=ParseMode.MARKDOWN
        )

def show_full_surah_page(query, surah_num, page):
    ar_ayahs, tr_ayahs = get_surah_ayahs(surah_num)
    if not ar_ayahs or not tr_ayahs:
        query.edit_message_text("❌ Не удалось загрузить суру. Попробуйте позже.")
        return

    page_size = 5
    start = page * page_size
    end = start + page_size

    surahs = get_surahs()
    surah_name = next((s['englishName'] for s in surahs if s['number'] == surah_num), f"Сура {surah_num}")

    text = f"📖 *{surah_name}* — аяты {start+1}–{min(end, len(ar_ayahs))}\n\n"

    for i in range(start, min(end, len(ar_ayahs))):
        ar = ar_ayahs[i]
        tr = tr_ayahs[i]
        text += f"*Аят {ar['numberInSurah']}*\n"
        text += f"{ar['text']}\n"
        text += f"_{tr['text']}_\n\n"

    keyboard = []

    nav_buttons = []
    if start > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"surah_full_{surah_num}_{page - 1}"))
    if end < len(ar_ayahs):
        nav_buttons.append(InlineKeyboardButton("➡️ Далее", callback_data=f"surah_full_{surah_num}_{page + 1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([
        InlineKeyboardButton("↩️ Назад к аятам", callback_data=f"surah_{surah_num}")
    ])
    keyboard.append([
        InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    ])

    query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
    if page == 0:
       bitrate = 128
       edition = "ar.alafasy"
       audio_url = f"https://cdn.islamic.network/quran/audio-surah/{bitrate}/{edition}/{surah_num}.mp3"
    try:
        query.message.reply_audio(
            audio=audio_url,
            title=f"Сура {surah_name}",
            caption=f"🎧 Аудио полной суры *{surah_name}*",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Ошибка при отправке полного аудио суры: {e}")
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрируем обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CallbackQueryHandler(handle_button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_ayah_request))

    print("🤖 Бот запущен!")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()