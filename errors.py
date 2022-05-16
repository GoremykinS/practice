# ошибки

class IncorrectDataRecivedError(Exception):
#     исключение - некорректные данные получены от сокета
    def __str__(self):
        return 'принято некорректное сообщение от удаленого компьютера'

class NonDictInputError(Exception):
    #     исключение - аргумент функции не словарь
    def __str__(self):
        return 'аргумент функции должен быть словарем.'

class ReqFieldMissingError(Exception):
    # ошибка  -отсутвие обязательного поля в принятом словаре

    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'в принятом словаре отсутвует обязательное поле {self.missing_field}.'




