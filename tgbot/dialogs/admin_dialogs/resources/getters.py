from aiogram_dialog import DialogManager

from infrastructure.database.repo.requests import RequestsRepo


async def library_getters(dialog_manager: DialogManager, **middleware_data):
    repo: RequestsRepo = middleware_data.get('repo')

    library_url = await repo.resources.get_url_library()

    return {
        "text": ("<b>Посилання на Life Library</b>\n"
                 "{library_url}").format(library_url=library_url)
    }