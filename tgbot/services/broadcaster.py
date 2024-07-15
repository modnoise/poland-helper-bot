import asyncio
import logging
from typing import Union

from aiogram import Bot
from aiogram import exceptions
from aiogram.enums import ContentType
from aiogram.types import InlineKeyboardMarkup


def get_execution_time_str_format(execution_time: float):
    if execution_time < 60:
        # Display execution time in seconds
        execution_time = f"{execution_time:.2f}"
        unit = "seconds"
    elif execution_time < 3600:
        # Display execution time in minutes and seconds
        minutes, seconds = divmod(execution_time, 60)
        execution_time = f"{int(minutes)}m {int(seconds)}s"
        unit = ""
    else:
        # Display execution time in hours and minutes
        hours, minutes = divmod(execution_time, 3600)
        minutes, seconds = divmod(minutes, 60)
        execution_time = f"{int(hours)}h {int(minutes)}m"
        unit = ""
    return execution_time, unit


async def send_message(
    content_type: ContentType,
    bot: Bot,
    user_id: Union[int, str],
    text: str,
    media_id: str = None,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    try:
        if content_type == ContentType.TEXT:
            await bot.send_message(
                user_id,
                text,
                disable_notification=disable_notification,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        if content_type == ContentType.PHOTO:
            await bot.send_photo(
                user_id,
                photo=media_id,
                caption=text,
                disable_notification=disable_notification,
                reply_markup=reply_markup,
            )
        if content_type == ContentType.VIDEO:
            await bot.send_video(
                user_id,
                video=media_id,
                caption=text,
                disable_notification=disable_notification,
                reply_markup=reply_markup,
            )
        if content_type == ContentType.DOCUMENT:
            await bot.send_document(
                user_id,
                document=media_id,
                caption=text,
                disable_notification=disable_notification,
                reply_markup=reply_markup,
            )
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_message(
            content_type, bot, user_id, text, media_id, disable_notification, reply_markup
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcast(
    content_type: ContentType,
    bot: Bot,
    users: list[Union[str, int]],
    text: str,
    media_id: str = None,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> int:
    """
    Simple broadcaster.
    :param bot: Bot instance.
    :param users: List of users.
    :param text: Text of the message.
    :param disable_notification: Disable notification or not.
    :param reply_markup: Reply markup.
    :return: Count of messages.
    """
    count = 0
    try:
        for user_id in users:
            if await send_message(
                content_type, bot, user_id, text, media_id, disable_notification, reply_markup
            ):
                count += 1
            await asyncio.sleep(
                0.05
            )  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count
