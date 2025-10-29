from aiogram import F
from bot_instance import dp
from keyboards.builder import SubMenu
from keyboards.deps import BackButton
from aiogram.types import CallbackQuery
from logger_setup import logger
from marzban.backend import BackendContext, MARZ_DATA
from misc.bot_setup import get_links

marz_back = BackendContext(*MARZ_DATA)


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
        
        text_reponse = "Здесь содержаться подписки"
        link = res.get('subscription_url') #type: ignore
        text_reponse += "\n"*2 + f"`{link}`"
        links_marz = res.get("links") #type: ignore
        links = await get_links(links_marz)

        await callback.message.edit_text( #type: ignore
            text=text_reponse,
            reply_markup=SubMenu.links_keyboard(links),
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

        links_marz = res.get("links") #type: ignore
        link = res.get("links")[int(sub_id)] #type: ignore
        sub_url = res.get('subscription_url') #type: ignore

        text_response = f"""
Здесь содержаться подписки:

<h1><code>{sub_url}</code></h1>{"\n"*2} <code>{link}</code>
"""
        links = await get_links(links_marz)
        await callback.message.edit_text( #type: ignore
            text=text_response,
            reply_markup=SubMenu.links_keyboard(links=links),
            parse_mode="HTML"
        )