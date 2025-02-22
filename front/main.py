from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from back.filter import LimitedTextInput10, LimitedTextInput4
from back.window_selector import WindowSelector


class TabContent(BoxLayout):
    def __init__(self, **kwargs):
        super(TabContent, self).__init__(orientation='vertical', padding=10, spacing=1, **kwargs)

        self.button_layout = BoxLayout(size_hint_y=None, height=50, padding=10, spacing=0)
        self.button1 = Button(text='Клавиатура')
        self.button2 = Button(text='Мышь', disabled=True)
        self.button_layout.add_widget(self.button1)
        self.button_layout.add_widget(self.button2)
        self.add_widget(self.button_layout)

        self.input_layout1 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        self.input_layout1.add_widget(Label(text='Введите повторы:'))
        self.number_input1 = LimitedTextInput4(multiline=False, input_filter='int')

        self.input_layout1.add_widget(self.number_input1)

        self.input_layout2 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        self.input_layout2.add_widget(Label(text='Введите задержку ms:'))
        self.number_input2 = LimitedTextInput4(multiline=False, input_filter='int', size_hint=(0.47, 1))
        self.number_input2_2 = LimitedTextInput4(multiline=False, input_filter='int', size_hint=(0.47, 1))
        self.input_layout2.add_widget(self.number_input2)
        self.input_layout2.add_widget(self.number_input2_2)

        self.input_layout3 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        self.input_layout3.add_widget(Label(text='Горячая клавиша:'))
        self.number_input3 = LimitedTextInput10(multiline=False)
        self.input_layout3.add_widget(self.number_input3)

        self.input_layout4 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.5))
        self.number_input4 = TextInput(multiline=True, hint_text='Введите последовательность через пробел')
        self.input_layout4.add_widget(self.number_input4)

        self.button_layout2 = BoxLayout(size_hint_y=None, height=50, padding=0, spacing=0)
        self.button_target = Button(text='таргет окна')
        self.button_target.bind(on_press=self.open_window_selector)
        self.button_Macro = Button(text='Запись макроса', disabled=True)
        self.button_layout2.add_widget(self.button_target)
        self.button_layout2.add_widget(self.button_Macro)

        self.button4 = Button(text='Запуск', size_hint=(1, 0.1))
        self.button4.bind(on_press=self.on_start)

        self.show_inputs()

        self.add_widget(self.input_layout1)
        self.add_widget(self.input_layout2)
        self.add_widget(self.input_layout3)
        self.add_widget(self.input_layout4)
        self.add_widget(self.button_layout2)
        self.add_widget(self.button4)

        self.button1.bind(on_press=self.toggle_inputs)

    def hide_inputs(self):
        '''Скрываем поля'''
        for layout in [self.input_layout1, self.input_layout2, self.input_layout3, self.input_layout4, self.button_layout2]:
            layout.opacity = 0
            layout.disabled = True

    def show_inputs(self):
        '''Показываем поля'''
        for layout in [self.input_layout1, self.input_layout2, self.input_layout3, self.input_layout4, self.button_layout2]:
            layout.opacity = 1
            layout.disabled = False

    def toggle_inputs(self, instance):
        '''Управляем полями'''
        if self.input_layout1.opacity == 0:
            self.show_inputs()
        else:
            self.hide_inputs()

    def on_start(self, instance):
        '''Собираем и передаем данные'''
        from back.main import Backender
        Backender.go(self, instance,
                     self.number_input4,
                     self.number_input3,
                     self.number_input2,
                     self.number_input2_2,
                     self.number_input1)

    def load_data(self, data):
        '''Запролняем поля'''
        self.number_input1.text = data.get('repeats', '')
        self.number_input2.text = data.get('delay1', '')
        self.number_input2_2.text = data.get('delay2', '')
        self.number_input3.text = data.get('hotkey', '')
        self.number_input4.text = data.get('sequence', '')

    def open_window_selector(self, instance):
        '''Новое окно таргета'''
        window_selector = WindowSelector(target_button=instance)
        window_selector.open()