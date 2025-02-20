import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
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

        # Кнопки для навигации
        self.nav_layout = BoxLayout(size_hint_y=None, height=30, padding=0, spacing=10)
        self.add_tab_button = Button(text='Добавить вкладку')
        self.del_tab_button = Button(text='Убрать вкладку')

        self.add_tab_button.bind(on_press=self.add_tab)  # Привязка события нажатия кнопки к методу добавления
        self.del_tab_button.bind(on_press=self.del_tab)  # Привязка события нажатия кнопки к методу удаления

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
        # Метод для добавления новой вкладки (максимум 6)
        if self.tab_counter < 6:  # Ограничение на 6 вкладок
            self.tab_counter += 1  # Увеличиваем счетчик вкладок
            self.tab_name = f'{self.tab_counter}'
            self.new_tab = TabbedPanelItem(text=self.tab_name)
            self.new_tab.add_widget(TabContent())  # Используем класс TabContent для наполнения новой вкладки
            self.tab_panel.add_widget(self.new_tab)

            # Проверяем, нужно ли отключать кнопку добавления
            if self.tab_counter >= 6:
                self.add_tab_button.disabled = True

            # Включаем кнопку удаления
            self.del_tab_button.disabled = False

    def del_tab(self, instance):
        """Метод для удаления вкладки с самым высоким числом в названии, кроме вкладки 'Инфо'."""
        # Создаем список вкладок, которые нужно удалить, исключая 'Инфо'
        tabs_to_remove = [tab for tab in self.tab_panel.tab_list if tab.text != 'Инфо']

        # Сортируем вкладки по числовому значению в названии (предполагается, что название - это число)
        tabs_to_remove.sort(key=lambda tab: int(tab.text), reverse=True)

        # Удаляем вкладку с самым высоким числом
        if tabs_to_remove:
            highest_tab = tabs_to_remove[0]  # Вкладка с самым высоким числом
            self.tab_panel.remove_widget(highest_tab)  # Удаляем вкладку
            self.tab_counter -= 1  # Уменьшаем счётчик вкладок
            print(f"Удалена вкладка: {highest_tab.text}, оставшиеся вкладки: {self.tab_counter}")  # Отладочное сообщение

            # Проверяем, нужно ли отключать кнопку удаления
            if self.tab_counter == 0:
                self.del_tab_button.disabled = True

            # Включаем кнопку добавления
            self.add_tab_button.disabled = False

        print("Нет вкладок для удаления, кроме 'Инфо'.")  # Отладочное сообщение

    def get_all_input_data(self):
        """Собирает данные из всех полей ввода во всех вкладках."""
        all_data = {}
        for tab in self.tab_panel.tab_list:
            # Предполагается, что каждая вкладка имеет экземпляр класса TabContent
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
        """Загружает данные из файла settings.json и создает вкладки в порядке возрастания."""
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                # Устанавливаем счётчик вкладок на количество элементов в data
                self.tab_counter = len(data)

                # Сортируем имена вкладок по возрастанию числового значения
                sorted_tab_names = sorted(data.keys(), key=lambda x: int(x))

                for tab_name in sorted_tab_names:
                    tab_data = data[tab_name]  # Получаем данные для текущей вкладки
                    # Создаем новую вкладку
                    new_tab = TabbedPanelItem(text=tab_name)
                    tab_content = TabContent()  # Создаем содержимое вкладки

                    # Заполняем поля ввода данными из tab_data
                    tab_content.load_data(tab_data)

                    new_tab.add_widget(tab_content)
                    self.tab_panel.add_widget(new_tab)  # Добавляем вкладку в таб-панель

                print("Настройки загружены:", data)
        except FileNotFoundError:
            print("Файл настроек не найден. Используйте значения по умолчанию.")
        except json.JSONDecodeError:
            print("Ошибка при чтении файла настроек. Проверьте формат.")


if __name__ == '__main__':
    MyApp().run()
