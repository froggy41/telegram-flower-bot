import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

PRODUCTS = {
    "rose": {"name": "Red Roses", "price": 25},
    "tulip": {"name": "Tulips", "price": 20},
}

async def create_invoice(title, amount):
    url = "https://pay.crypt.bot/api/createInvoice"
    headers = {"Crypto-Pay-API-Token": CRYPTO_API_KEY}
    payload = {"asset": "USDT", "amount": amount, "description": title}
    r = requests.post(url, headers=headers, json=payload)
    return r.json()["result"]["pay_url"]

@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🌹 Buy Roses", callback_data="buy_rose"))
    keyboard.add(types.InlineKeyboardButton("🌷 Buy Tulips", callback_data="buy_tulip"))
    await message.answer("Welcome to our Flower Shop 🌸", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery):
    product = callback.data.replace("buy_", "")
    item = PRODUCTS[product]
    url = await create_invoice(item["name"], item["price"])
    await callback.message.answer(
        f"💳 Pay here: {url}"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
