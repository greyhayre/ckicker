import random
import pyautogui
from kivy.clock import Clock
import logging
import keyboard


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
            button.disabled = False
            look1.disabled=True
            look2.disabled=True
            look3.disabled=True
            look4.disabled=True
            look5.disabled=True
            Backender.running = True
            Backender.execute_sequence(sequence, repeats, delay_1, delay_2)
        else:
            button.text = 'Запуск'
            button.disabled = False
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
                    delay_time = action[1:-1].strip()
                    try:
                        delay_time = float(delay_time)
                        logging.info(f'[INFO] [Запланирована задержка] {delay_time} секунд')
                        Clock.schedule_once(Backender.perform_action, delay_time)
                        Backender.index += 1
                    except ValueError:
                        logging.error(f'[ERROR] Ошибка преобразования задержки: {delay_time}')
                        Backender.index += 1
                else:
                    logging.info(f'[INFO] [Выполняем действие] {action}')
                    try:
                        # Проверяем наличие вложенных действий
                        if '(' in action and ')' in action:
                            main_action, sub_actions = action.split('(', 1)
                            sub_actions = sub_actions[:-1]  # Убираем закрывающую скобку
                            main_action = main_action.strip()
                            sub_actions = sub_actions.strip()

                            # Нажимаем основное действие (например, любую клавишу)
                            pyautogui.keyDown(main_action)

                            # Обрабатываем вложенные действия, разделенные запятыми
                            sub_action_list = [sub_action.strip() for sub_action in sub_actions.split(',') if sub_action.strip()]

                            # Функция для выполнения поддействий с задержкой
                            def execute_sub_actions(index):
                                if index < len(sub_action_list):
                                    sub_action = sub_action_list[index]
                                    logging.info(f'[INFO] [Выполняем поддействие] {sub_action}')
                                    if sub_action:  # Проверяем, что поддействие не пустое
                                        pyautogui.press(sub_action)
                                    # Запланируем следующее поддействие с задержкой
                                    Clock.schedule_once(lambda dt: execute_sub_actions(index + 1), 0.1)  # 10ms задержка

                            # Запускаем выполнение поддействий
                            execute_sub_actions(0)

                            # Отпускаем основное действие после выполнения всех поддействий
                            Clock.schedule_once(lambda dt: pyautogui.keyUp(main_action), len(sub_action_list) * 0.1)

                        else:
                            # Если нет скобок, выполняем действие как обычно
                            actions = action.split('+')
                            pyautogui.hotkey(*[a.strip() for a in actions])

                    except Exception as e:
                        logging.error(f'[ERROR] Ошибка при нажатии на кнопки {action}: {e}')

                    Backender.index += 1
                    Backender.schedule_random_delay()
            else:
                Backender.index = 0
                Backender.current_repeat += 1
                Backender.schedule_random_delay()
    def schedule_random_delay():
        delay = random.uniform(Backender.delay_1, Backender.delay_2)
        logging.info(f'Запланирована задержка: {delay:.2f} секунд')  # Логирование
        Clock.schedule_once(Backender.perform_action, delay)
