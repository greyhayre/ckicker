import random
import pyautogui
from kivy.clock import Clock

class Backender:
    @staticmethod
    def go(tab_content):
        # Получаем данные из полей ввода
        repeats_input = tab_content.number_input1.text
        repeats = int(repeats_input) if repeats_input else float('inf')
        delay_1 = int(tab_content.number_input2.text) if tab_content.number_input2.text else 10
        delay_2 = int(tab_content.number_input2_2.text) if tab_content.number_input2_2.text else 30
        sequence = (tab_content.number_input4.text).split(' ')

        # Запускаем процесс с задержками
        Backender.execute_sequence(sequence, repeats, delay_1, delay_2)

    @staticmethod
    def execute_sequence(sequence, repeats, delay_1, delay_2):
        Backender.index = 0
        Backender.repeats = repeats
        Backender.sequence = sequence
        Backender.delay_1 = delay_1 / 1000  # Преобразуем в секунды
        Backender.delay_2 = delay_2 / 1000  # Преобразуем в секунды
        Backender.current_repeat = 0

        # Запускаем выполнение
        Clock.schedule_once(Backender.perform_action, 0)

    @staticmethod
    def perform_action(dt):
        if Backender.current_repeat < Backender.repeats:
            if Backender.index < len(Backender.sequence):
                action = Backender.sequence[Backender.index].strip()

                # Проверяем, является ли действие задержкой
                if action.startswith('[') and action.endswith(']'):
                    # Извлекаем значение задержки
                    delay_time = action[1:-1].strip()  # Убираем скобки и пробелы
                    try:
                        delay_time = float(delay_time)  # Преобразуем в число
                        print(f'Дополнительная задержка: {delay_time} секунд')  # Отладка
                        Clock.schedule_once(Backender.perform_action, delay_time)
                        Backender.index += 1  # Увеличиваем индекс, чтобы перейти к следующему действию
                    except ValueError:
                        print(f'Ошибка преобразования задержки: {delay_time}')  # Обработка ошибок
                        Backender.index += 1  # Переходим к следующему действию, если ошибка
                else:
                    print(f'Выполняем действие: {action}')  # Отладка: показываем текущее действие
                    try:
                        pyautogui.press(action)
                    except Exception as e:
                        print(f'Ошибка при нажатии на кнопку {action}: {e}')

                    Backender.index += 1

                    # Запланируем случайную задержку перед выполнением следующего действия
                    delay = random.uniform(Backender.delay_1, Backender.delay_2)
                    print(f'Запланирована задержка: {delay:.2f} секунд')  # Отладка
                    Clock.schedule_once(Backender.perform_action, delay)
            else:
                Backender.index = 0
                Backender.current_repeat += 1
                delay = random.uniform(Backender.delay_1, Backender.delay_2)
                print(f'Запланирована задержка перед следующим циклом: {delay:.2f} секунд')  # Отладка
                Clock.schedule_once(Backender.perform_action, delay)

