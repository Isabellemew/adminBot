from aiogram import Bot, Dispatcher, types, executor
import requests
import json
from datetime import datetime, timedelta
import os

API_TOKEN = '7257032872:AAGrW1dPt1T-Rh3BhDX3Xvtk0_fK3OXHrNo'
FIRST_BOT_API = 'http://<8009133089:AAEg5N6v_CF46jot2ppx2t7zfKPPa-p6wTs>:3000/api/announcements?token=your_secret_token'
ANNOUNCE_FILE = 'announcements.json'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Загрузка и сохранение анонсов

def load_announcements():
    if os.path.exists(ANNOUNCE_FILE):
        with open(ANNOUNCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_announcements(announcements):
    with open(ANNOUNCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(announcements, f, ensure_ascii=False, indent=2)

# Удаление старых анонсов

def cleanup_announcements():
    announcements = load_announcements()
    now = datetime.now()
    announcements = [a for a in announcements if datetime.strptime(a['date'], '%Y-%m-%d %H:%M:%S') > now - timedelta(days=14)]
    save_announcements(announcements)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Анонсы мероприятий')
    await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Анонсы мероприятий')
async def ask_announcement(message: types.Message):
    await message.answer("Напишите объявление для мероприятий:")
    dp.register_message_handler(save_announcement, content_types=types.ContentTypes.TEXT, state=None)

async def save_announcement(message: types.Message):
    cleanup_announcements()
    text = message.text
    announcements = load_announcements()
    announcements.append({'text': text, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    save_announcements(announcements)
    # Отправка в первый бот через API
    try:
        requests.post(FIRST_BOT_API, json={'announcement': text})
    except Exception:
        pass
    await message.answer("Анонс сохранён и отправлен!")
    dp.message_handlers.unregister(save_announcement)

if __name__ == '__main__':
    executor.start_polling(dp)
