from aiogram import F
from bot_instance import dp
from keyboards.builder import SubMenu
from keyboards.deps import BackButton
from aiogram.types import CallbackQuery
from logger_setup import logger
from marzban.backend import BackendContext, MARZ_DATA
from misc.utils import to_link

marz_back = BackendContext(*MARZ_DATA)
text_pattern = """
Здесь содержаться подписки:
(Нажмите для копирования)

"""


@dp.callback_query(F.data == "subs")
async def main_subs(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал Subs")

    async with marz_back as backend: #type: ignore
        res = await backend.get_user(user_id)
        if res is None:
            await callback.message.edit_text( #type: ignore
            text="Пусто",
            reply_markup=BackButton.back_subs()
        )
        data = await to_link(res) #type: ignore

        text_reponse = text_pattern
        text_reponse += "\n"*2 + f"`{data.sub_link}`" #type: ignore

        await callback.message.edit_text( #type: ignore
            text=text_reponse,
            reply_markup=SubMenu.links_keyboard(data.titles), #type: ignore
            parse_mode="MARKDOWN"
        )

@dp.callback_query(F.data.startswith("sub_"))
async def process_sub(callback: CallbackQuery):
    sub_id = callback.data.replace("sub_", "") #type: ignore
    user_id = str(callback.from_user.id)
    logger.info(f"ID : {user_id} | Нажал {callback.data}")


    async with marz_back as backend: #type: ignore
        res = await backend.get_user(user_id)
        if res is None:
            await callback.message.edit_text( #type: ignore
            text="Пусто",
            reply_markup=BackButton.back_subs()
        )
        logger.info(res)
        
        data = await to_link(res) #type: ignore

        links_marz = data.links #type: ignore
        sub_url = data.sub_link #type: ignore

        link = links_marz[int(sub_id)] #type: ignore

        text_response = f"""{text_pattern}
<code>{sub_url}</code>{"\n"*2} <code>{link}</code>
"""
        await callback.message.edit_text( #type: ignore
            text=text_response,
            reply_markup=SubMenu.links_keyboard(links=data.titles), #type: ignore
            parse_mode="HTML"
        )