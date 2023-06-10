from typing import Union, TypeVar, Optional

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from aiogram.types import Message

from database.methods import Methods

# Binding types
ReplyMarkup = TypeVar(
    'ReplyMarkup',
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)


async def user_active_group_answer(
        msg: Message,
        methods: Optional[Methods] = None,
        user_message: Optional[str] = None,
        user_markup: Optional[Union[ReplyMarkup]] = None,
        other_message: Optional[str] = None,
        other_markup: Union[ReplyMarkup] = None,
) -> None:
    bot: Bot = msg.bot

    # If no Methods object is passed
    if methods is None:
        methods = Methods(msg.from_user.id)

    # Sending a message only if it contains text
    if user_message is not None:
        await msg.answer(text=user_message, reply_markup=user_markup)

    if other_message is not None:
        for user in methods.active_group_another_users:
            await bot.send_message(user.tg_id, text=other_message, reply_markup=other_markup)


async def get_full_name_by_tg_id(bot: Bot, tg_id: int) -> str:
    user = await bot.get_chat(tg_id)
    return user.full_name


