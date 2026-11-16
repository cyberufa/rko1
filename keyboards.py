from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from banks_data import BANKS


def get_main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏦 Выбрать банк для РКО", callback_data="catalog")
    builder.button(text="📊 Сравнить условия", callback_data="compare")
    builder.adjust(1)
    return builder.as_markup()


def get_banks_list_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for bank_id, bank_info in BANKS.items():
        builder.button(
            text=f"🔹 {bank_info['name']}",
            callback_data=f"bank_{bank_id}"
        )
    builder.button(text="⬅️ В главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


def get_bank_card_kb(ref_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # Кнопка с прямой реферальной ссылкой
    builder.row(
        InlineKeyboardButton(text="🚀 Открыть счёт (перейти на сайт)", url=ref_url)
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ К списку банков", callback_data="catalog")
    )
    return builder.as_markup()


def get_back_to_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏦 Перейти к выбору банка", callback_data="catalog")
    builder.button(text="⬅️ В главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()