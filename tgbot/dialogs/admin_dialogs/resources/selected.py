import re
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.admin_dialogs.resources.states import Resources


async def on_edit_library_url_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Resources.edit_library_url)


async def on_entered_library_url(message: Message, widget: TextInput, manager: DialogManager, result_input: str):
    repo: RequestsRepo = manager.middleware_data.get('repo')
    url_pattern = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')
    if bool(url_pattern.match(result_input)):
        await repo.resources.update_url_library(result_input)
        await message.answer("Посилання успішно змінено ✅")
        await manager.switch_to(Resources.library)
        return

    await message.answer(
        text="Вибачте, але виглядає, що ви ввели неправильне посилання. Будь ласка, спробуйте знову."
    )



