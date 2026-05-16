import re
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery,
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from forms.mpg import Form

router = Router()

def get_main_inline_start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Конвертувати MPG у Л/100 км", callback_data="convert_mpg")],
            [InlineKeyboardButton(text="🔄 Конвертувати милі у км", callback_data="convert_m")]
        ]
    )
    return keyboard

def get_cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Головне меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_main_inline_dev_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Сайт розробника", url="https://www.linkedin.com/in/myroslav-dzyadzo?utm_source=share_via&utm_content=profile&utm_medium=member_android")]
        ]
    )
    return keyboard


@router.message(Command("start"))
@router.message(F.text.lower() == "старт")
async def start(message: Message):
    await message.answer(
        f"👋 Привіт! 😃 <b>{message.from_user.first_name}</b>\n\n"
        f"🚀 Радий тебе бачити! Напиши /help для підказки 💡\n"
        f"⚡️ Для швидкого переходу до розрахунків натисніть кнопку нижче 👇",
        parse_mode="HTML", 
        reply_markup=get_main_inline_start_keyboard()
    )

@router.message(Form.waiting_for_mpg, Command("cancel"))
@router.message(Form.waiting_for_m, Command("cancel"))
@router.message(Form.waiting_for_mpg, F.text == "🔙 Головне меню")
@router.message(Form.waiting_for_m, F.text == "🔙 Головне меню")
async def cancel_conversion(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ <b>Розрахунки скасовано.</b>\nПовертаємось до головного меню.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "⚡️ Для швидкого переходу до розрахунків натисніть кнопку нижче 👇",
        reply_markup=get_main_inline_start_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "convert_mpg")
async def start_mpg_conversion(callback: CallbackQuery, state: FSMContext):
    await callback.answer() 
    await callback.message.answer(
        "🧮 <b>Конвертер MPG ➡️ Л/100 км</b>\n\n"
        "Будь ласка, введіть значення розходу в <b>MPG</b> (милях на галон).\n"
        "<i>(Приклад: 25 або 31.5)</i>",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Form.waiting_for_mpg)


@router.message(Form.waiting_for_mpg, lambda msg: not re.match(r"^\d+([.,]\d+)?$", msg.text.strip()))
async def process_mpg_invalid(message: Message):
    await message.answer(
        "⚠️ <b>Помилка!</b> Введіть коректне числове значення.\n"
        "Наприклад: <code>24</code> або <code>32.8</code>",
        parse_mode="HTML"
    )
    
@router.message(Form.waiting_for_mpg, F.text)
async def process_mpg_calculation(message: Message, state: FSMContext):
    raw_text = message.text.strip().replace(",", ".")
    mpg_value = float(raw_text)
    
    if mpg_value <= 0:
        await message.answer("❌ Значення MPG має бути більшим за 0. Спробуйте ще раз:")
        return

    l_per_100km = 235.215 / mpg_value

    await message.answer(
        f"🔄 <b>Результат конвертації:</b>\n\n"
        f"🇺🇸 <b>{mpg_value} MPG</b> 🌍 еквівалентно приблизно:\n"
        f"➡️ <b>{l_per_100km:.2f} Л/100 км</b> ⛽️",
        parse_mode="HTML"
    )
    
@router.callback_query(F.data == "convert_m")
async def start_m_conversion(callback: CallbackQuery, state: FSMContext):
    await callback.answer() 
    await callback.message.answer(
        "🧮 <b>Конвертер милі ➡️ км</b>\n\n"
        "Будь ласка, введіть значення в <b>Mилі</b>.\n"
        "<i>(Приклад: 25 або 31.5)</i>",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Form.waiting_for_m)

@router.message(Form.waiting_for_m, lambda m: not re.match(r"^\d+([.,]\d+)?$", m.text.strip()))
async def process_m_invalid(message: Message):
    await message.answer(
        "⚠️ <b>Помилка!</b> Введіть коректне числове значення.\n"
        "Наприклад: <code>24</code> або <code>32.8</code>",
        parse_mode="HTML"
    )
    
@router.message(Form.waiting_for_m, F.text)
async def process_m_calculation(message: Message, state: FSMContext):
    raw_text = message.text.strip().replace(",", ".")
    m_value = float(m_text) if (m_text := raw_text) else 0.0
    m_value = float(raw_text)
    
    if m_value <= 0:
        await message.answer("❌ Значення має бути більшим за 0. Спробуйте ще раз:")
        return

    km = 1.60934 * m_value

    await message.answer(
        f"🔄 <b>Результат конвертації:</b>\n\n"
        f"🇺🇸 <b>{m_value} милі</b> 🌍 еквівалентно приблизно:\n"
        f"➡️ <b>{km:.2f} км</b>",
        parse_mode="HTML"
    )

@router.message(Command("help"))
@router.message(F.text.lower() == "список команд")
async def help_command(message: Message):
    await message.answer(
        "📜 <b>Список команд:</b>\n\n"
        "▶️ /start — Запуск бота\n"
        "❓ /help — Підказки та допомога\n"
        "ℹ️ /about — Про розробника та проект",
        parse_mode="HTML",
    )
    
@router.message(Command("about"))
@router.message(F.text.lower() == "про нас")
async def about(message: Message):
    await message.answer(
        "ℹ️ <b>Інформація:</b>\n\n"
        "🛡 © Всі права захищені.\n"
        "👨‍💻 Розробник: <b>Dzyadzo Myroslav</b>",
        parse_mode="HTML",
        reply_markup=get_main_inline_dev_keyboard()
    )
  
@router.message()
async def echo_message(message: Message):
    await message.answer(
        f"👋 Привіт! 😃 <b>{message.from_user.first_name}</b>\n\n"
        f"⚠️ Ти ввів текст. Будь ласка, використовуй команди з меню! 🛠",
        parse_mode="HTML"
    )
