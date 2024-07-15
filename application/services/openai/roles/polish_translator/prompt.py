from langchain_core.prompts import PromptTemplate

def get_translator_prompt(user_language: str):
    match user_language:
        case "uk":
            template = """Система: Нижче наведено дружню розмову між людиною та польським викладачем/перекладачем. Надайте розгорнуту відповідь на запитання в контексті польської мови. Дай відповідь у форматі TELEGRAM HTML.
                        
                Поточна розмова:
                {history}
        
                Питання: {input}
                Корисна відповідь:
                """
        case "ru":
            template = """Система: Ниже приводится дружеская беседа между человеком и преподавателем/переводчиком польского языка. Дайте развернутый ответ на вопрос в контексте польского языка. Дай ответ в формате TELEGRAM HTML
                
                Текущий разговор:
                {history}
                
                Вопрос: {input}
                Полезный ответ:"""
        case _:
            template = """System: Below is a friendly conversation between a person and a Polish teacher/translator. Provide an extended response to the question in the context of the Polish language. Format answer in TELEGRAM HTML format

            Current conversation:
            {history}

            Question: {input}
            Helpful Answer:
            """

    return PromptTemplate(
        input_variables=["input", "history"],
        template=template)
