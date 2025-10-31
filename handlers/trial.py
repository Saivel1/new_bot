from aiogram import F
from bot_instance import dp
from aiogram.types import CallbackQuery
from logger_setup import logger
from misc.utils import get_user, modify_user, calculate_expire, create_user
from db.database import async_session
from db.db_models import UserOrm
from repositories.base import BaseRepository
from datetime import timedelta
from config_data.config import settings
from keyboards.deps import BackButton


@dp.callback_query(F.data == 'trial')
async def trial_activate(callback: CallbackQuery):
    user_id = callback.from_user.id 
    logger.info(f'Пользователь {user_id} нажал пробный период')

    await callback.message.edit_text(text="⏳ Загрузка 0%") #type: ignore

    await callback.message.edit_text( #type: ignore
        text="Активируем пробный период"
    )

    user = await get_user(user_id=user_id)
    if not user:
        user = await create_user(user_id=user_id, username=callback.from_user.username)
    
    await callback.message.edit_text(text="⏳ Загрузка 30%") #type: ignore
    if user.trial_used:
        await callback.answer()
        await callback.message.edit_text( #type: ignore
            text='Пробный период уже был активирован'
        )
        return

    await callback.message.edit_text(text="⏳ Загрузка 50%") #type: ignore
    await callback.message.answer("🎉")
    async with async_session() as session:
        repo = BaseRepository(session=session, model=UserOrm)
        user = await repo.update_one({
            "trial_used": True
        }, user_id=str(user_id))
        old_expire = user.subscription_end #type: ignore

    new_expire = calculate_expire(old_expire=old_expire)    
    add_days = new_expire + timedelta(days=settings.TRIAL_DAYS) #type: ignore

    await callback.answer()
    user_modification = await modify_user(username=user_id, expire=add_days)
    await callback.message.edit_text(text="✅ Загрузка 100%") #type: ignore

    if user_modification:
        await callback.message.edit_text( #type: ignore
            text='Пробный период активирован ✅',
            reply_markup=BackButton.back_start()
        )
    else:
        await callback.message.edit_text( #type: ignore
                text='Возникла ошибка нажмите /start'
        )