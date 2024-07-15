from aiogram.fsm.state import StatesGroup, State


class ConnectHub(StatesGroup):
    menu = State()
    request_for_expert = State()
    request_confirmation = State()
    provide_questionnaire = State()
    questionnaire_confirmation = State()