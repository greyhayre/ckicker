from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.core.window import Window
from front.main import TabContent


height = 600
width = 400


class MyApp(App):
    def build(self):
        Window.size = (width, height)

        self.tab_counter = 0  # Счетчик для новых вкладок
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Создание меню выбора вкладки
        self.tab_panel = TabbedPanel(tab_width=(width/7)-3, do_default_tab=False)
        self.default_tab = TabbedPanelItem(text='Инфо')
        self.tab_panel.add_widget(self.default_tab)
        self.default_tab.add_widget(Label(text='Краткое инфо'))

        # Кнопки для добавления новых вкладок
        self.add_tab_button = Button(text='Добавить вкладку', size_hint=(1, 0.1))
        self.add_tab_button.bind(on_press=self.add_tab)  # Привязка события нажатия кнопки к методу

        self.main_layout.add_widget(self.tab_panel)
        self.main_layout.add_widget(self.add_tab_button)

        return self.main_layout

    def add_tab(self, instance):
        # Метод для добавления новой вкладки Ограничение 6
        if self.tab_counter <= 5:
            self.tab_name = f'{self.tab_counter + 1}'
            self.new_tab = TabbedPanelItem(text=self.tab_name)
            self.new_tab.add_widget(TabContent())  # Используем класс TabContent для наполнения новой вкладки
            self.tab_panel.add_widget(self.new_tab)
            self.tab_counter += 1  # Увеличиваем счетчик вкладок
        else:
            self.add_tab_button.disabled = True

if __name__ == '__main__':
    MyApp().run()
