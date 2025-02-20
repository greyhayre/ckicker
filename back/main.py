class Backender:
    @staticmethod
    def go(tab_content):
        # Получаем данные из полей ввода
        repeats = tab_content.number_input1.text
        delay_1 = tab_content.number_input2.text
        delay_2 = tab_content.number_input2_2.text
        hotkey = tab_content.number_input3.text
        sequence = tab_content.number_input4.text

        # Пример: выводим данные в консоль
        print(f'Повторы: {repeats}, Задержка: {delay_1} до {delay_2}, Горячая клавиша: {hotkey}, Последовательность: {sequence}')
