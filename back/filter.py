from kivy.uix.textinput import TextInput


class LimitedTextInput4(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Проверяем, не превышает ли длина текста максимальное значение
        if len(self.text) + len(substring) > 4:  # Ограничение в 4 символа
            substring = substring[:4 - len(self.text)]  # Обрезаем лишние символы
        super().insert_text(substring, from_undo=from_undo)


class LimitedTextInput10(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Проверяем, не превышает ли длина текста максимальное значение
        if len(self.text) + len(substring) > 10:  # Ограничение в 4 символа
            substring = substring[:10 - len(self.text)]  # Обрезаем лишние символы
        super().insert_text(substring, from_undo=from_undo)
