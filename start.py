import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.core.window import Window
from front.main import TabContent
from back.window_selector import WindowSelector  # Импортируем класс WindowSelector

height = 600
width = 400

class MyApp(App):
    def build(self):
        Window.size = (width, height)

        self.tab_counter = 0  # Счетчик для новых вкладок
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Кнопки для навигации
        self.nav_layout = BoxLayout(size_hint_y=None, height=30, padding=0, spacing=10)
        self.add_tab_button = Button(text='Добавить вкладку')
        self.del_tab_button = Button(text='Убрать вкладку')

        self.add_tab_button.bind(on_press=self.add_tab)
        self.del_tab_button.bind(on_press=self.del_tab)

        self.nav_layout.add_widget(self.add_tab_button)
        self.nav_layout.add_widget(self.del_tab_button)

        # Создание меню выбора вкладки
        self.tab_panel = TabbedPanel(tab_width=(width/7)-3, do_default_tab=False)
        self.default_tab = TabbedPanelItem(text='Инфо')
        self.tab_panel.add_widget(self.default_tab)
        self.default_tab.add_widget(Label(text='Краткое инфо'))

        self.main_layout.add_widget(self.nav_layout)
        self.main_layout.add_widget(self.tab_panel)

        self.load_settings()

        return self.main_layout

    def add_tab(self, instance):
        if self.tab_counter < 6:
            self.tab_counter += 1
            self.tab_name = f'{self.tab_counter}'
            self.new_tab = TabbedPanelItem(text=self.tab_name)
            self.new_tab.add_widget(TabContent())
            self.tab_panel.add_widget(self.new_tab)

            if self.tab_counter >= 6:
                self.add_tab_button.disabled = True

            self.del_tab_button.disabled = False

    def del_tab(self, instance):
        tabs_to_remove = [tab for tab in self.tab_panel.tab_list if tab.text != 'Инфо']
        tabs_to_remove.sort(key=lambda tab: int(tab.text), reverse=True)

        if tabs_to_remove:
            highest_tab = tabs_to_remove[0]
            self.tab_panel.remove_widget(highest_tab)
            self.tab_counter -= 1
            print(f"Удалена вкладка: {highest_tab.text}, оставшиеся вкладки: {self.tab_counter}")

            if self.tab_counter == 0:
                self.del_tab_button.disabled = True

            self.add_tab_button.disabled = False

        print("Нет вкладок для удаления, кроме 'Инфо'.")

    def get_all_input_data(self):
        """Собирает данные из всех полей ввода во всех вкладках."""
        all_data = {}
        for tab in self.tab_panel.tab_list:
            if isinstance(tab.content, TabContent):
                tab_data = {
                    'repeats': tab.content.number_input1.text,
                    'delay1': tab.content.number_input2.text,
                    'delay2': tab.content.number_input2_2.text,
                    'hotkey': tab.content.number_input3.text,
                    'sequence': tab.content.number_input4.text
                }
                all_data[tab.text] = tab_data  # Сохраняем данные для каждой вкладки

        return all_data

    def on_stop(self):
        """Собирает данные и сохраняет их при закрытии приложения."""
        all_data = self.get_all_input_data()
        with open('data.json', 'w') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print("Данные сохранены:", all_data)

    def load_settings(self):
        """Загружает данные из файла data.json и создает вкладки в порядке возрастания."""
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.tab_counter = len(data)

                sorted_tab_names = sorted(data.keys(), key=lambda x: int(x))

                for tab_name in sorted_tab_names:
                    tab_data = data[tab_name]
                    new_tab = TabbedPanelItem(text=tab_name)
                    tab_content = TabContent()
                    tab_content.load_data(tab_data)

                    new_tab.add_widget(tab_content)
                    self.tab_panel.add_widget(new_tab)

                print("Настройки загружены:", data)
        except FileNotFoundError:
            print("Файл настроек не найден. Используйте значения по умолчанию.")
        except json.JSONDecodeError:
            print("Ошибка при чтении файла настроек. Проверьте формат.")

    def open_window_selector(self, instance):
        """Открывает окно выбора для выбора активного окна."""
        window_selector = WindowSelector()
        window_selector.open()  # Открываем окно выбора

if __name__ == '__main__':
    MyApp().run()