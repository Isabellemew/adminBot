import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import requests
import json
from datetime import datetime, timedelta
import os

API_TOKEN = '7257032872:AAGrW1dPt1T-Rh3BhDX3Xvtk0_fK3OXHrNo'
FIRST_BOT_API = 'http://localhost:8080/add_event'
ANNOUNCE_FILE = 'announcements.json'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
user_states = {}

def load_announcements():
    if os.path.exists(ANNOUNCE_FILE):
        with open(ANNOUNCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_announcements(announcements):
    with open(ANNOUNCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(announcements, f, ensure_ascii=False, indent=2)

def cleanup_announcements():
    announcements = load_announcements()
    now = datetime.now()
    announcements = [a for a in announcements if datetime.strptime(a['date'], '%Y-%m-%d %H:%M:%S') > now - timedelta(days=14)]
    save_announcements(announcements)

@dp.message(Command('start'))
async def send_welcome(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Event Announcements')]
    ])
    await message.answer("Welcome to the admin panel!", reply_markup=keyboard)

@dp.message(lambda message: message.text == 'Event Announcements')
async def ask_announcement(message: Message):
    user_states[message.from_user.id] = 'waiting_for_announcement'
    await message.answer("Please enter your event announcement:")

@dp.message()
async def save_announcement(message: Message):
    if user_states.get(message.from_user.id) == 'waiting_for_announcement':
        cleanup_announcements()
        text = message.text
        announcements = load_announcements()
        announcements.append({'text': text, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        save_announcements(announcements)
        # Send to the first bot via API
        try:
            resp = requests.post(FIRST_BOT_API, json={'text': text}, timeout=5)
            if resp.status_code == 200:
                await message.answer("Announcement saved and sent!")
            else:
                await message.answer(f"Failed to send to the first bot: {resp.status_code} {resp.text}")
        except Exception as e:
            await message.answer(f"Failed to send to the first bot: {e}")
        user_states[message.from_user.id] = None

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
