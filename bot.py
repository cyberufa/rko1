import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from banks_data import BANKS
from keyboards import (
    get_main_menu_kb,
    get_banks_list_kb,
    get_bank_card_kb,
    get_back_to_menu_kb
)

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


WELCOME_TEXT = (
    "👋 <b>Добро пожаловать в сервис подбора РКО для бизнеса!</b>\n\n"
    "Здесь собраны актуальные предложения от ведущих банков для ИП и ООО "
    "с бесплатным открытием и обслуживанием.\n\n"
    "Выберите действие ниже:"
)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text=WELCOME_TEXT,
        reply_markup=get_main_menu_kb()
    )


@dp.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text=WELCOME_TEXT,
        reply_markup=get_main_menu_kb()
    )
    await callback.answer()


@dp.callback_query(F.data == "catalog")
async def cb_catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        text="🏦 <b>Выберите банк</b>, чтобы посмотреть условия тарифа и подать заявку онлайн:",
        reply_markup=get_banks_list_kb()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("bank_"))
async def cb_bank_detail(callback: CallbackQuery):
    bank_id = callback.data.split("_", 1)[1]
    bank = BANKS.get(bank_id)

    if not bank:
        await callback.answer("Банк не найден", show_alert=True)
        return

    text = (
        f"🏦 <b>{bank['name']}</b>\n\n"
        f"📌 <b>Тариф:</b> {bank['tariff']}\n"
        f"💰 <b>Стоимость:</b> {bank['price']}\n\n"
        f"<b>Преимущества:</b>\n{bank['features']}\n\n"
        f"<i>Нажмите кнопку ниже, чтобы оставить заявку на официальном сайте банка.</i>"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=get_bank_card_kb(bank["ref_url"])
    )
    await callback.answer()


@dp.callback_query(F.data == "compare")
async def cb_compare(callback: CallbackQuery):
    lines = ["📊 <b>Краткое сравнение стартовых тарифов:</b>\n"]
    for bank in BANKS.values():
        lines.append(f"• <b>{bank['name']}</b> — {bank['price']}")

    lines.append("\nВыберите конкретный банк, чтобы узнать детали и оформить счёт.")
    await callback.message.edit_text(
        text="\n".join(lines),
        reply_markup=get_back_to_menu_kb()
    )
    await callback.answer()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())