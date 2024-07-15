from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from tgbot.dialogs.admin_dialogs.menu_dialogs.states import AdminMenu
from tgbot.filters.admin import AdminFilter
from tgbot.filters.chat_types import IsChat
from tgbot.states import GetMedia

admin_router = Router()
admin_router.message.filter(IsChat())
admin_router.callback_query.filter(IsChat())

admin_router.message.filter(AdminFilter())
admin_router.callback_query.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def send_admin_menu(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await state.clear()
    await dialog_manager.reset_stack(True)
    await dialog_manager.start(AdminMenu.show_menu)


@admin_router.message(Command("media"))
async def get_file_id(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await state.set_state(GetMedia.get_file)
    await message.answer("Send media")


@admin_router.message(StateFilter(GetMedia.get_file))
async def get_file_id(message: Message, state: FSMContext):
    await state.clear()
    file_id = "Error"

    if message.photo:
        file_id = message.photo[0].file_id

    if message.video:
        file_id = message.video.file_id

    if message.document:
        file_id = message.document.file_id

    if message.animation:
        file_id = message.animation.file_id

    if message.voice:
        file_id = message.voice.file_id

    if message.audio:
        file_id = message.audio.file_id

    if message.video_note:
        file_id = message.video_note.file_id

    await message.answer(file_id)
