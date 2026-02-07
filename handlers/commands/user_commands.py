from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext
from app.storage.UpdateProfileClass import UpdateProfile
from app.database.crud import update_profile
from aiogram.fsm.context import FSMContext
from app.keyboards.btn_select_gender import get_user_gender_keyboard
from app.keyboards.btn_floor_select import get_user_floor_keyboard

router = Router(name=__name__)



@router.message(Command("profile"))
async def starting_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
):

    await message.answer(i18n.get("profile-title"))
    await state.set_state(UpdateProfile.name)
    await message.answer(i18n.get("profile-name"))



@router.message(UpdateProfile.name)
async def send_name(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
):
    tg_id = message.from_user.id


    name = message.text
    await update_profile(tg_id=tg_id, name=name)
    await state.set_state(UpdateProfile.age)
    await message.answer(i18n.get("profile-age", name=name))



@router.message(UpdateProfile.age)
async def send_age(
    message: Message,
    i18n: I18nContext,
    state: FSMContext
):
    tg_id = message.from_user.id


    age = message.text.strip()
    try:
        user_age = int(age)
        await update_profile(tg_id=tg_id, age=user_age)
    except ValueError:
        await state.set_state(UpdateProfile.age)
        await message.answer(i18n.get("profile-age-not-int"))
        return

    await state.set_state(UpdateProfile.country)
    await message.answer(i18n.get("profile-country"))



@router.message(UpdateProfile.country)
async def send_country(
    message: Message,
    i18n: I18nContext,
    state: FSMContext
):
    tg_id = message.from_user.id


    country = message.text
    await update_profile(tg_id=tg_id, country=country)
    await state.set_state(UpdateProfile.gender)
    await message.answer(
        i18n.get("profile-gender"),
        reply_markup=get_user_gender_keyboard()
    )



@router.callback_query(UpdateProfile.gender)
async def send_gender(
    call: CallbackQuery,
    i18n: I18nContext,
    state: FSMContext,
):
    tg_id = call.from_user.id


    gender = call.data
    await update_profile(tg_id=tg_id, gender=gender)
    await state.set_state(UpdateProfile.looking)
    await call.message.answer(
        i18n.get("profile-looking"),
        reply_markup=get_user_floor_keyboard()
    )
    await call.answer()



@router.callback_query(UpdateProfile.looking)
async def send_looking(
    call: CallbackQuery,
    i18n: I18nContext,
    state: FSMContext
):
    tg_id = call.from_user.id

    floor = call.data
    await update_profile(tg_id=tg_id, floor=floor)
    await state.set_state(UpdateProfile.yourself)
    await call.message.answer(i18n.get("profile-yourself"))
    await call.answer()



@router.message(UpdateProfile.yourself)
async def send_yourself(
    message: Message,
    i18n: I18nContext,
    state: FSMContext
):
    tg_id = message.from_user.id


    yourself = message.text
    await update_profile(tg_id=tg_id, yourself=yourself)
    await state.set_state(UpdateProfile.user_photo)
    await message.answer(i18n.get("profile-yourphoto"))



@router.message(UpdateProfile.user_photo, F.photo)
async def send_photo(
    message: Message,
    i18n: I18nContext,
    state: FSMContext
):
    tg_id = message.from_user.id

    photo_id = message.photo[-1].file_unique_id
    await update_profile(tg_id=tg_id, photo_user=photo_id)
    await state.clear()
    await message.answer(i18n.get("profile-success"))