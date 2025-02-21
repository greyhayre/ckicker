import random
import pyautogui
from kivy.clock import Clock
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO)

class Backender:
    running = False  # Флаг для отслеживания состояния выполнения
    action_scheduled = False  # Флаг для отслеживания запланированных действий

    @staticmethod
    def go(tab_content, button, look1, look2, look3, look4, look5):
        # Получаем данные из полей ввода
        repeats_input = tab_content.number_input1.text
        repeats = int(repeats_input) if repeats_input else float('inf')
        delay_1 = int(tab_content.number_input2.text) if tab_content.number_input2.text else 10
        delay_2 = int(tab_content.number_input2_2.text) if tab_content.number_input2_2.text else 30
        sequence = (tab_content.number_input4.text).split(' ')

        # Переключаем состояние кнопки
        if not Backender.running:
            button.text = 'Стоп'
            look1.disabled=True
            look2.disabled=True
            look3.disabled=True
            look4.disabled=True
            look5.disabled=True
            Backender.running = True
            Backender.execute_sequence(sequence, repeats, delay_1, delay_2)
        else:
            button.text = 'Запуск'
            Backender.running = False
            look1.disabled=False
            look2.disabled=False
            look3.disabled=False
            look4.disabled=False
            look5.disabled=False
            # Остановка выполнения не нужна, просто изменяем текст кнопки

    @staticmethod
    def execute_sequence(sequence, repeats, delay_1, delay_2):
        Backender.index = 0
        Backender.repeats = repeats
        Backender.sequence = sequence
        Backender.delay_1 = delay_1 / 1000  # Преобразуем в секунды
        Backender.delay_2 = delay_2 / 1000  # Преобразуем в секунды
        Backender.current_repeat = 0

        # Запускаем выполнение
        Backender.schedule_next_action()

    @staticmethod
    def schedule_next_action():
        if Backender.running:
            # Запускаем выполнение
            Clock.schedule_once(Backender.perform_action, 0)

    @staticmethod
    def perform_action(dt):
        if Backender.current_repeat < Backender.repeats and Backender.running:
            if Backender.index < len(Backender.sequence):
                action = Backender.sequence[Backender.index].strip()

                # Проверяем, является ли действие задержкой
                if action.startswith('[') and action.endswith(']'):
                    # Извлекаем значение задержки
                    delay_time = action[1:-1].strip()  # Убираем скобки и пробелы
                    try:
                        delay_time = float(delay_time)  # Преобразуем в число
                        logging.info(f'Дополнительная задержка: {delay_time} секунд')  # Логирование
                        Clock.schedule_once(Backender.perform_action, delay_time)
                        Backender.index += 1  # Увеличиваем индекс, чтобы перейти к следующему действию
                    except ValueError:
                        logging.error(f'Ошибка преобразования задержки: {delay_time}')  # Обработка ошибок
                        Backender.index += 1  # Переходим к следующему действию, если ошибка
                else:
                    logging.info(f'Выполняем действие: {action}')  # Логирование
                    try:
                        # Разделяем действия, если они указаны через +
                        actions = action.split('+')
                        # Пробуем нажимать одновременно все указанные клавиши
                        pyautogui.hotkey(*[a.strip() for a in actions])
                    except Exception as e:
                        logging.error(f'Ошибка при нажатии на кнопки {action}: {e}')
                    
                    Backender.index += 1  # Переходим к следующему действию                                 



                    # Запланируем случайную задержку перед выполнением следующего действия
                    Backender.schedule_random_delay()
            else:
                Backender.index = 0
                Backender.current_repeat += 1
                Backender.schedule_random_delay()

    @staticmethod
    def schedule_random_delay():
        delay = random.uniform(Backender.delay_1, Backender.delay_2)
        logging.info(f'Запланирована задержка: {delay:.2f} секунд')  # Логирование
        Clock.schedule_once(Backender.perform_action, delay)
