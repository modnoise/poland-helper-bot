from aiogram import types, Bot


async def set_user_defaults_commands(chat_id: int, bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command="start", description="🤖 Bot launch"),
    ],
        scope=types.BotCommandScopeChat(chat_id=chat_id),
    )


async def set_user_start_commands(chat_id: int, bot: Bot, lang: str):
    if lang == 'uk':
        await set_user_start_commands_uk(chat_id, bot)
    elif lang == 'ru':
        await set_user_start_commands_ru(chat_id, bot)
    else:
        await set_user_start_commands_en(chat_id, bot)


async def set_user_start_commands_en(chat_id: int, bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command="start", description="🤖 Bot launch"),
        types.BotCommand(command="chat", description="💡 Get consultation"),
        types.BotCommand(command="support", description="🛟 Support"),
        types.BotCommand(command="language", description="🌎 Change language"),

    ],
        scope=types.BotCommandScopeChat(chat_id=chat_id),
    )


async def set_user_start_commands_ru(chat_id: int, bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command="start", description="🤖 Запуск бота"),
        types.BotCommand(command="chat", description="💡 Получить консультацию"),
        types.BotCommand(command="support", description="🛟 Поддержка"),
        types.BotCommand(command="language", description="🌎 Изменить язык")
    ],
        scope=types.BotCommandScopeChat(chat_id=chat_id),
    )


async def set_user_start_commands_uk(chat_id: int, bot: Bot):
    await bot.set_my_commands(commands=[
        types.BotCommand(command="start", description="🤖 Запуск бота"),
        types.BotCommand(command="chat", description="💡 Отримати консультацію"),
        types.BotCommand(command="support", description="🛟 Підтримка"),
        types.BotCommand(command="language", description="🌎 Змінити мову"),
    ],
        scope=types.BotCommandScopeChat(chat_id=chat_id),
    )