from aiogram import Router
from aiogram.types import MessageReactionUpdated
from core.setup import bot

router = Router()
# Обработчик реакций
@router.message_reaction()
async def handle_reactions(event: MessageReactionUpdated):
    chat_id = event.chat.id
    message_id = event.message_id
    
    old_reactions = event.old_reaction
    new_reactions = event.new_reaction
    
    # Извлекаем эмодзи из реакций
    old_emojis = [r.emoji for r in old_reactions if hasattr(r, 'emoji')]
    new_emojis = [r.emoji for r in new_reactions if hasattr(r, 'emoji')]
    
    
    # Проверяем, какие эмодзи были добавлены/удалены
    added = [emoji for emoji in new_emojis if emoji not in old_emojis]
    removed = [emoji for emoji in old_emojis if emoji not in new_emojis]
    
    if added:
        print(f"Добавлены реакции: {added}")
        
    if removed:
        print(f"Удалены реакции: {removed}")
    
    # Проверка на конкретные эмодзи
    positive_emojis = ['👍', '❤️', '😍', '🔥', '🎉', '👏']
    negative_emojis = ['👎', '💩', '😠', '🤮', '🤡']
    
    for emoji in added:
        if emoji in positive_emojis:
            await bot.send_message(
                chat_id=chat_id,
                text=f"Спасибо за положительную реакцию {emoji}!",
                reply_to_message_id=message_id
            )
        elif emoji in negative_emojis:
            await bot.send_message(
                chat_id=chat_id,
                text=f"Ой, не понравилось {emoji}? Сорян!",
                reply_to_message_id=message_id
            )
