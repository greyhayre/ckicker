import json
import os

class SettingsManager:
    def __init__(self, filename='settings.json'):
        self.filename = filename
        self.settings = {}

    def load_settings(self):
        """Загрузка настроек из JSON файла."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.settings = json.load(file)
        else:
            self.settings = {}  # Если файл не существует, создаем пустой словарь

    def save_settings(self):
        """Сохранение настроек в JSON файл."""
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key, default=None):
        """Получение значения настройки по ключу."""
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        """Установка значения настройки по ключу."""
        self.settings[key] = value