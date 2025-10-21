import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import requests

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()



def get_random_dog_image():
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    data = response.json()
    return data["message"]



def get_dragons():
    url = "https://api.spacexdata.com/v3/dragons"
    response = requests.get(url)
    return response.json()

def get_dragon_info(name):
    dragons = get_dragons()
    for dragon in dragons:
        if dragon["name"].lower() == name.lower():
            return dragon
    return None

def get_dragon_image(dragon):
    images = dragon.get("flickr_images", [])
    if images:
        return images[0]
    return None


@dp.message(CommandStart())
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐕 Фото собаки")],
            [KeyboardButton(text="🚀 Корабли SpaceX")],
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Привет! 👋\nВыбери действие на клавиатуре ниже:",
        reply_markup=keyboard
    )


@dp.message(F.text == "🐕 Фото собаки")
async def send_dog_image(message: Message):
    image_url = get_random_dog_image()
    await message.answer_photo(photo=image_url, caption="Вот тебе пёсик 🐾")

@dp.message(F.text == "🚀 Корабли SpaceX")
async def send_dragons_list(message: Message):
    dragons = get_dragons()
    buttons = [KeyboardButton(text=dragon["name"]) for dragon in dragons]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True
    )
    await message.answer("Выбери корабль 🚀:", reply_markup=keyboard)

@dp.message()
async def send_dragon_info(message: Message):
    dragon_name = message.text
    dragon_info = get_dragon_info(dragon_name)
    if dragon_info:
        dragon_image = get_dragon_image(dragon_info)
        info = (
            f"🚀 {dragon_info['name']}\n"
            f"Тип: {dragon_info['type']}\n"
            f"Экипаж: {dragon_info.get('crew_capacity', 'неизвестно')}\n"
            f"Продолжительность полёта (лет): {dragon_info.get('orbit_duration_yr', 'неизвестно')}\n"
            f"Масса (кг): {dragon_info.get('dry_mass_kg', 'неизвестно')}\n"
            f"Активен: {'Да' if dragon_info['active'] else 'Нет'}"
        )
        if dragon_image:
            await message.answer_photo(photo=dragon_image, caption=info)
        else:
            await message.answer(info)
    else:
        await message.answer("Выбери кнопку или корабль из списка 👇")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())