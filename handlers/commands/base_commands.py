from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram_i18n import I18nContext
from aiogram.fsm.context import FSMContext
from app.database.crud import insert_lang 
from app.keyboards.btn_langs import get_language_keyboard

router = Router(name=__name__)

@router.message(CommandStart())
async def boting_starting(
    message: Message,
    state: FSMContext,
    i18n: I18nContext,
    user_session: dict | None = None
):
    state_data = await state.get_data()
    has_session = user_session and state_data.get('user_session')

    if has_session:
        session_data = state_data['user_session']
        counter = session_data.get('counter', 0)
        session_data['counter'] = counter + 1
        
        # Обязательно сохраняем изменения в FSM!
        await state.update_data(user_session=session_data)
        
        await message.answer(i18n.welcome())
    else:
        # Нет сессии — показываем кнопки выбора языка
        await message.answer(
            "Select language:",
            reply_markup=get_language_keyboard()  # Кнопки должны отображаться
        )


@router.callback_query(F.data.in_(["en", "de"]))
async def select_lang(call: CallbackQuery, i18n: I18nContext):
    language = call.data
    user_id = call.from_user.id
    user_name = call.from_user.username
    if user_name is None:
        await call.message.answer(f"⚠️De: Es ist unmöglich, sich ohne Benutzernamen zu registrieren.\n"
                                  f"En: It is impossible to register without a username.⚠️")
        return
    result = await insert_lang(user_id, language, user_name)
    if result:
        await call.message.answer(i18n.get("lang-success"))
