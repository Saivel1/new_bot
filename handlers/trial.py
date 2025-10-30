from aiogram import F
from bot_instance import dp
from aiogram.types import CallbackQuery
from logger_setup import logger
from misc.utils import get_user
from db.database import async_session
from db.db_models import UserOrm
from repositories.base import BaseRepository

@dp.callback_query(F.data == 'trial')
async def trial_activate(callback: CallbackQuery):
    user_id = callback.from_user.id 
    logger.info(f'Пользователь {user_id} нажал пробный период')

    user = await get_user(user_id=user_id)
    if not user:
        await callback.message.edit_text( #type: ignore
            text='Возникла внутренняя ошибка, попробуйте нажать /start и нажать снова.'
        )
        raise ValueError
    
    async with async_session() as session:
        repo = BaseRepository(session=session, model=UserOrm)
        await repo.update_one({
            "trial_used": True
        }, user_id=str(user_id))
    
    await callback.message.edit_text( #type: ignore
        text='Пробный период активирован'
    )