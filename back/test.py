import logging
import pyautogui
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import keyboard  # Не забудьте установить эту библиотеку

class Backender:
    current_repeat = 0
    repeats = 1
    running = False
    index = 0
    sequence = []

    @staticmethod
    def perform_action(dt):
        if Backender.current_repeat < Backender.repeats and Backender.running:
            if Backender.index < len(Backender.sequence):
                action = Backender.sequence[Backender.index].strip()

                # Логика выполнения действий...
                # (оставьте вашу логику здесь)

                Backender.index += 1
            else:
                Backender.index = 0
                Backender.current_repeat += 1

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Поле для ввода
        self.number_input3 = TextInput(multiline=False)
        layout.add_widget(self.number_input3)

        # Кнопка для запуска макроса
        self.button4 = Button(text='Запуск', size_hint=(1, 0.1))
        self.button4.bind(on_press=self.on_start)
        layout.add_widget(self.button4)

        # Установка горячей клавиши
        keyboard.add_hotkey('ctrl+shift+m', self.on_start)  # Замените на вашу горячую клавишу

        return layout

    def on_start(self, instance=None):
        if not Backender.running:
            Backender.running = True
            logging.info('[INFO] Макрос запущен.')
            Clock.schedule_once(Backender.perform_action, 0)
        else:
            Backender.running = False
            logging.info('[INFO] Макрос остановлен.')

if __name__ == '__main__':
    MyApp().run()


