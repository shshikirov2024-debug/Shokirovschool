"""
Shokirov School Telegram kanali uchun kunlik avtomatik post bot.
Har kuni (GitHub Actions cron orqali) ishga tushadi va bir nechta kanalga:
1. Farg'ona shahri uchun kunlik ob-havo ma'lumotini
2. Ta'lim/o'quv bo'yicha kunlik foydali maslahat yoki yangilikni
yuboradi.

Kerakli maxfiy ma'lumotlar (GitHub repo -> Settings -> Secrets and variables -> Actions):
TELEGRAM_BOT_TOKEN     - BotFather'dan olingan token
TELEGRAM_CHANNEL_ID    - Birinchi kanal (masalan: @shokirovschool)
TELEGRAM_CHANNEL_ID_2  - Ikkinchi kanal (masalan: @zamonaviyfiziklar)

Ob-havo manbasi: Open-Meteo (bepul, API kalit talab qilmaydi)
"""
import os
import sys
from datetime import datetime
import requests

# ---------- Sozlamalar ----------
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")
TELEGRAM_CHANNEL_ID_2 = os.environ.get("TELEGRAM_CHANNEL_ID_2")

# Farg'ona shahri koordinatalari
CITY_NAME = "Farg'ona"
LATITUDE = 40.3894
LONGITUDE = 71.7864
TIMEZONE = "Asia/Tashkent"

WEATHER_CODE_MAP = {
    0: "Ochiq, quyoshli ☀️",
    1: "Asosan ochiq 🌤",
    2: "Qisman bulutli ⛅",
    3: "Bulutli ☁️",
    45: "Tuman 🌫",
    48: "Muzli tuman 🌫",
    51: "Yengil mayda yomg'ir 🌦",
    53: "Mayda yomg'ir 🌦",
    55: "Kuchli mayda yomg'ir 🌧",
    61: "Yengil yomg'ir 🌧",
    63: "Yomg'ir 🌧",
    65: "Kuchli yomg'ir 🌧",
    71: "Yengil qor ❄️",
    73: "Qor ❄️",
    75: "Kuchli qor ❄️❄️",
    80: "Jala 🌦",
    81: "Kuchli jala 🌧",
    82: "Juda kuchli jala ⛈",
    95: "Momaqaldiroq ⛈",
    96: "Do'l bilan momaqaldiroq ⛈",
    99: "Kuchli do'l bilan momaqaldiroq ⛈",
}

EDU_TIPS = [
    "📌 Har kuni 30 daqiqa takrorlash, bir marta 5 soat o'qishdan ko'ra samaraliroq. Muntazamlik — muvaffaqiyat kaliti!",
    "📌 Test yechayotganda avval oson savollarni belgilab, keyin qiyinlariga qayting — vaqtni tejaysiz.",
    "📌 Yangi mavzuni o'rgangandan so'ng, uni o'z so'zlaringiz bilan qayta tushuntirib ko'ring — bu eslab qolishni mustahkamlaydi.",
    "📌 Matematikada formulani yodlashdan ko'ra, uning qayerdan kelib chiqqanini tushunish uzoq muddatga foyda beradi.",
    "📌 Kuniga kamida 10 ta yangi so'z o'rganish, bir yilda 3600 dan ortiq so'z boyligini beradi.",
    "📌 Imtihon oldidan yaxshi uxlash, tunni bedor o'tkazishdan ko'ra miya faoliyatiga foydaliroq.",
    "📌 O'z bilim darajangizni tekshirish uchun har hafta kichik mock-test yeching — zaif tomonlaringizni aniqlaysiz.",
    "📌 Pomodoro texnikasi: 25 daqiqa diqqat bilan ishlash + 5 daqiqa tanaffus — samaradorlikni oshiradi.",
    "📌 Xato qilishdan qo'rqmang — har bir xato qaysi mavzuni yana takrorlash kerakligini ko'rsatadi.",
    "📌 Kunlik rejangizni kechqurun emas, ertalab tuzing — miya yangi kun uchun tayyor bo'ladi.",
]


def get_weather() -> str:
    """Open-Meteo API orqali Farg'ona uchun bugungi ob-havoni oladi."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        code = data["daily"]["weathercode"][0]
        t_max = round(data["daily"]["temperature_2m_max"][0])
        t_min = round(data["daily"]["temperature_2m_min"][0])
        description = WEATHER_CODE_MAP.get(code, "Ma'lumot mavjud emas")
        return (
            f"🌤 <b>{CITY_NAME} uchun bugungi ob-havo</b>\n\n"
            f"{description}\n"
            f"🌡 Kunduzi: {t_max}°C | Kechasi: {t_min}°C"
        )
    except Exception as e:  # noqa: BLE001
        print(f"Ob-havo ma'lumotini olishda xatolik: {e}", file=sys.stderr)
        return f"🌤 <b>{CITY_NAME} uchun bugungi ob-havo</b>\n\nHozircha ma'lumot olinmadi."


def get_edu_tip() -> str:
    day_index = datetime.now().timetuple().tm_yday
    tip = EDU_TIPS[day_index % len(EDU_TIPS)]
    return f"🎓 <b>Kunlik ta'lim maslahati</b>\n\n{tip}"


def build_message() -> str:
    today = datetime.now().strftime("%d.%m.%Y")
    parts = [
        f"📅 <b>{today}</b>\n",
        get_weather(),
        "",
        get_edu_tip(),
        "",
        "📞 Murojaat uchun: +998 91 670 33 37 | +998 90 836 22 33",
        "🏫 Shokirov School | Ta'lim va tarbiya maskani",
    ]
    return "\n".join(parts)


def send_to_telegram(text: str, channel_id: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not channel_id:
        print(
            "XATOLIK: TELEGRAM_BOT_TOKEN yoki channel_id o'rnatilmagan.",
            file=sys.stderr,
        )
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    resp = requests.post(url, data=payload, timeout=15)
    if resp.status_code != 200:
        print(f"[{channel_id}] Telegramga yuborishda xatolik: {resp.status_code} {resp.text}", file=sys.stderr)
    else:
        print(f"[{channel_id}] Post muvaffaqiyatli yuborildi.")


if __name__ == "__main__":
    message = build_message()
    print("--- Yuborilayotgan xabar ---")
    print(message)
    print("----------------------------")

    if not TELEGRAM_BOT_TOKEN:
        print("XATOLIK: TELEGRAM_BOT_TOKEN o'rnatilmagan.", file=sys.stderr)
        sys.exit(1)

    channels = [c for c in [TELEGRAM_CHANNEL_ID, TELEGRAM_CHANNEL_ID_2] if c]
    if not channels:
        print("XATOLIK: hech qanday kanal ID o'rnatilmagan.", file=sys.stderr)
        sys.exit(1)

    for ch in channels:
        send_to_telegram(message, ch)
