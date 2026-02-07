from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.database.crud import all_users
router = Router(name=__name__)

@router.message(Command("admin", prefix="/!"))
async def admin_panel(message: Message):
    select_all_users = await all_users()
    
    # Собираем всех пользователей в один текст
    result_text = "В боте зарегистрировались:\n\n"
    for index, username in enumerate(select_all_users, start=1):
        result_text += f"{index}. @{username}\n"
    
    result_text += f"\nВсего: {len(select_all_users)} пользователей"
    
    await message.answer(result_text)