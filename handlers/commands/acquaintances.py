from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select
from app.database.models.user import User
from app.database.models.base import AsyncSession
from aiogram_i18n import I18nContext



router = Router()

@router.message(Command("acquaintances"))

async def acquaintances(message: Message, session: AsyncSession, i18n: I18nContext):
    # Получаем текущего пользователя
    current_user = await session.execute(
        select(User).where(User.tg_id == message.from_user.id)
    )
    current_user = current_user.scalars().first()
    
    if not current_user:
        return

    # Определяем целевой пол
    target_gender = 'woman' if current_user.gender == 'man' else 'man'

    # Формируем запрос
    query = select(User).where(
        User.gender == target_gender,
        User.tg_id != message.from_user.id
    )
    
    result = await session.execute(query)
    users = result.scalars().all()

    if not users:
        await message.answer(i18n.get("profile-questionnaires"))
        return

    # Отправляем каждого пользователя отдельно
    for user in users:
        response = (
            f"Имя: {user.name}\n"
            f"Возраст: {user.age}\n"
            f"Пол: {user.gender}\n"
            f"О себе: {user.yourself}\n"
            f"Страна: {user.country}\n"
        )
        
        if user.photo_user:  # Проверяем наличие фото
            await message.answer_photo(user.photo_user, caption=response)
        else:
            await message.answer(response)
