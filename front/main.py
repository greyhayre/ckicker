from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.core.window import Window

# Установка размера окна
height = 550
width = 400
Window.size = (width, height)

class TabContent(BoxLayout):
    def __init__(self, **kwargs):
        super(TabContent, self).__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        # Добавление кнопок в одну линию
        button_layout = BoxLayout(size_hint_y=None, height=50, padding=10, spacing=0)
        button1 = Button(text='Клавиатура')
        button2 = Button(text='Мышь', disabled=True)
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)

        self.add_widget(button_layout)

        # Поля ввода
        input_layout1 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        input_layout1.add_widget(Label(text='Введите повторы:'))
        self.number_input1 = TextInput(multiline=False, input_filter='int')
        input_layout1.add_widget(self.number_input1)
        self.add_widget(input_layout1)

        input_layout2 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        input_layout2.add_widget(Label(text='Введите задержку:'))
        self.number_input2 = TextInput(multiline=False, input_filter='int')
        input_layout2.add_widget(self.number_input2)
        self.add_widget(input_layout2)

        input_layout3 = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.5))
        self.number_input3 = TextInput(multiline=False, hint_text='Введите последовательность через пробел')
        input_layout3.add_widget(self.number_input3)
        self.add_widget(input_layout3)

        button_target = Button(text='таргет окна', size_hint=(1, 0.1), disabled=True)
        self.add_widget(button_target)

        button3 = Button(text='Запись макроса', size_hint=(1, 0.1), disabled=True)
        button4 = Button(text='Запуск', size_hint=(1, 0.1))

        self.add_widget(button3)
        self.add_widget(button4)

class MyApp(App):
    def build(self):
        self.tab_counter = 1  # Счетчик для новых вкладок
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Создание меню выбора вкладки
        self.tab_panel = TabbedPanel()

        # Создание первой вкладки
        tab1 = TabbedPanelItem(text='Вкладка 1')
        tab1.add_widget(TabContent())  # Добавляем содержимое первой вкладки
        self.tab_panel.add_widget(tab1)

        # Кнопки для добавления новых вкладок
        add_tab_button = Button(text='Добавить вкладку', size_hint=(1, 0.1))
        add_tab_button.bind(on_press=self.add_tab)  # Привязка события нажатия кнопки к методу

        main_layout.add_widget(self.tab_panel)
        main_layout.add_widget(add_tab_button)

        return main_layout

    def add_tab(self, instance):
        # Метод для добавления новой вкладки
        tab_name = f'Вкладка {self.tab_counter + 1}'
        new_tab = TabbedPanelItem(text=tab_name)
        new_tab.add_widget(TabContent())  # Используем класс TabContent для наполнения новой вкладки
        self.tab_panel.add_widget(new_tab)
        self.tab_counter += 1  # Увеличиваем счетчик вкладок

if __name__ == '__main__':
    MyApp().run()
