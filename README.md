# Shokirov School — Kunlik avtomatik post bot

Bu bot har kuni ertalab soat **08:00 (Toshkent/Farg'ona vaqti)** da
`@shokirovschool` kanaliga avtomatik ravishda:

- Farg'ona shahri uchun kunlik ob-havo ma'lumotini,
- ta'lim bo'yicha kunlik foydali maslahatni

yuboradi. Bot **GitHub Actions** orqali ishlaydi — sizga alohida server
yoki doim yoqiq kompyuter kerak emas, hammasi bepul.

## O'rnatish (5 qadam)

### 1. Telegram bot yaratish
1. Telegramda **@BotFather** ga yozing.
2. `/newbot` buyrug'ini yuboring, botga nom va username bering
   (masalan: `ShokirovSchoolDailyBot`).
3. BotFather sizga **token** beradi (masalan:
   `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`) — uni saqlab qo'ying.

### 2. Botni kanalga admin qilib qo'shish
1. `@shokirovschool` kanaliga o'ting -> **Administrators** -> **Add Administrator**.
2. Yangi yaratgan botni qidiring va qo'shing.
3. Bot kamida **"Post messages"** huquqiga ega bo'lishi kerak.

### 3. Bu loyihani GitHub'ga yuklash
1. [github.com](https://github.com) da yangi **repository** yarating
   (masalan: `shokirov-bot`), Public yoki Private — farqi yo'q.
2. Shu papkadagi barcha fayllarni (`bot.py`, `requirements.txt`,
   `.github/workflows/daily_post.yml`) o'sha repoga yuklang.
   - Eng oson yo'l: GitHub sahifasida **"Add file" -> "Upload files"**
     tugmasidan foydalanib, fayllarni sudrab tashlash (drag & drop).
   - `.github/workflows/daily_post.yml` faylini albatta xuddi shu
     papka tuzilishida saqlang (papkalar nomini o'zgartirmang).

### 4. Maxfiy ma'lumotlarni (Secrets) qo'shish
1. Repo sahifasida: **Settings -> Secrets and variables -> Actions**.
2. **"New repository secret"** tugmasi orqali ikkita secret qo'shing:
   - Nomi: `TELEGRAM_BOT_TOKEN` — qiymati: BotFather bergan token
   - Nomi: `TELEGRAM_CHANNEL_ID` — qiymati: `@shokirovschool`

### 5. Sinab ko'rish
1. Repo sahifasida **Actions** bo'limiga o'ting.
2. Chap tomondan **"Kunlik post - Shokirov School"** workflow'ni tanlang.
3. **"Run workflow"** tugmasini bosing — bot darhol ishga tushadi va
   kanalga test post yuboradi.
4. Agar xatolik chiqsa, shu workflow ishga tushgan qatorni ochib,
   qizil (xato) qismini o'qing — odatda token yoki channel ID noto'g'ri
   kiritilganidan bo'ladi.

Shundan keyin bot **har kuni soat 08:00 da** (hech narsa qilmasangiz ham)
avtomatik ishlab turadi.

## Sozlash

- **Vaqtni o'zgartirish**: `.github/workflows/daily_post.yml` faylidagi
  `cron: "0 3 * * *"` qatorini o'zgartiring. Diqqat: bu vaqt **UTC**
  bo'yicha, Toshkent/Farg'ona vaqti UTC+5, ya'ni UTC vaqtiga 5 soat
  qo'shsangiz mahalliy vaqt chiqadi (masalan, mahalliy 18:00 kerak
  bo'lsa — `cron: "0 13 * * *"`).
- **Shaharni o'zgartirish**: `bot.py` faylidagi `LATITUDE` va
  `LONGITUDE` qiymatlarini kerakli shahar koordinatalariga almashtiring.
- **Ta'lim maslahatlarini qo'shish/o'zgartirish**: `bot.py` faylidagi
  `EDU_TIPS` ro'yxatiga istalgancha yangi matn qo'shishingiz mumkin.
- **Matn formatini o'zgartirish**: `build_message()` funksiyasi ichida
  postning umumiy ko'rinishini (murojaat raqamlari, imzo va h.k.)
  tahrirlashingiz mumkin.

## Eslatma

Ob-havo ma'lumoti **Open-Meteo** (bepul, ro'yxatdan o'tish shart emas)
xizmatidan olinadi, shuning uchun qo'shimcha API kalit talab qilinmaydi.
