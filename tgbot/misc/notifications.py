from typing import Union, List
from aiogram import md
from aiogram_broadcaster import TextBroadcaster


async def startup_notify(chats: Union[List[int], List[str], int, str]) -> None:
    # Generate chats
    chats = [
        {
            "chat_id": chat_id,
            "mention": md.hlink(title=f"ID:{chat_id}", url=f"tg://user?id={chat_id}"),
        }
        for chat_id in chats
    ]

    # Run broadcaster
    await TextBroadcaster(
        chats=chats,
        text=md.hbold("$mention, The bot is running!"),
    ).run()
