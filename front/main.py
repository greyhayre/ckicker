from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Установка размера окна
height = 600
width = 400


class TabContent(BoxLayout):
    def __init__(self, **kwargs):
        super(TabContent, self).__init__(orientation='vertical', padding=10, spacing=1, **kwargs)

        # Добавление кнопок в одну линию
        self.button_layout = BoxLayout(size_hint_y=None, height=50, padding=10, spacing=0)
        self.button1 = Button(text='Клавиатура')
        self.button2 = Button(text='Мышь', disabled=True)
        self.button_layout.add_widget(self.button1)
        self.button_layout.add_widget(self.button2)
        self.add_widget(self.button_layout)

        # Поля ввода
        self.input_layout1 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        self.input_layout1.add_widget(Label(text='Введите повторы:'))
        self.number_input1 = TextInput(multiline=False, input_filter='int')
        self.input_layout1.add_widget(self.number_input1)
        self.add_widget(self.input_layout1)

        self.input_layout2 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        self.input_layout2.add_widget(Label(text='Введите задержку ms:'))
        self.number_input2 = TextInput(multiline=False, input_filter='int', size_hint=(0.47, 1))
        self.number_input2_2 = TextInput(multiline=False, input_filter='int', size_hint=(0.47, 1))
        self.input_layout2.add_widget(self.number_input2)
        self.input_layout2.add_widget(self.number_input2_2)
        self.add_widget(self.input_layout2)

        self.input_layout3 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        self.input_layout3.add_widget(Label(text='Горячая клавиша:'))
        self.number_input3 = TextInput(multiline=False)
        self.input_layout3.add_widget(self.number_input3)
        self.add_widget(self.input_layout3)

        self.input_layout4 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.5))
        self.number_input4 = TextInput(multiline=False, hint_text='Введите последовательность через пробел')
        self.input_layout4.add_widget(self.number_input4)
        self.add_widget(self.input_layout4)

        # Добавление кнопок в одну линию
        self.button_layout2 = BoxLayout(size_hint_y=None, height=50, padding=0, spacing=0)
        self.button_target = Button(text='таргет окна', disabled=True)
        self.button_Macro = Button(text='Запись макроса', disabled=True)
        self.button_layout2.add_widget(self.button_target)
        self.button_layout2.add_widget(self.button_Macro)
        self.add_widget(self.button_layout2)

        self.button4 = Button(text='Запуск', size_hint=(1, 0.1))
        self.button4.bind(on_press=self.on_start)
        self.add_widget(self.button4)

    def on_start(self, instance):
        from back.main import Backender  # Импортируем здесь, чтобы избежать циклического импорта
        Backender.go(self)  # Передаем текущий экземпляр TabContent в метод go
