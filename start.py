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

        # Кнопки для добавления новых вкладок
        self.add_tab_button = Button(text='Добавить вкладку', size_hint=(1, 0.1))
        self.add_tab_button.bind(on_press=self.add_tab)  # Привязка события нажатия кнопки к методу

        # Создание меню выбора вкладки
        self.tab_panel = TabbedPanel(tab_width=(width/7)-3, do_default_tab=False)
        self.default_tab = TabbedPanelItem(text='Инфо')
        self.tab_panel.add_widget(self.default_tab)
        self.default_tab.add_widget(Label(text='Краткое инфо'))

        # Кнопки для навигации
        self.nav_layout = BoxLayout(size_hint_y=None, height=30, padding=0, spacing=10)
        self.add_tab_button = Button(text='Добавить вкладку')
        self.del_tab_button = Button(text='Убрать вкладку', disabled=True)
        self.add_tab_button.bind(on_press=self.add_tab)  # Привязка события нажатия кнопки к методу создания
        self.del_tab_button.bind(on_press=self.del_tab)  # Привязка события нажатия кнопки к методу удаления

        self.nav_layout.add_widget(self.add_tab_button)
        self.nav_layout.add_widget(self.del_tab_button)

        self.main_layout.add_widget(self.nav_layout)
        self.main_layout.add_widget(self.tab_panel)

        return self.main_layout

    def add_tab(self, instance):
        # Метод для добавления новой вкладки Ограничение 6
        if self.tab_counter < 6:  # Изменено на < 6 для ограничения 6 вкладок
            self.tab_name = f'{self.tab_counter + 1}'
            self.new_tab = TabbedPanelItem(text=self.tab_name)
            self.new_tab.add_widget(TabContent())  # Используем класс TabContent для наполнения новой вкладки
            self.tab_panel.add_widget(self.new_tab)
            self.tab_counter += 1  # Увеличиваем счетчик вкладок
            
            # Проверяем, нужно ли отключать кнопку добавления
            if self.tab_counter >= 6:
                self.add_tab_button.disabled = True
            
            # Включаем кнопку удаления
            self.del_tab_button.disabled = False

    def del_tab(self, instance):
        # Находим первую вкладку, которая не "Инфо"
        for tab in self.tab_panel.tab_list:
            if tab.text != 'Инфо':
                self.tab_panel.remove_widget(tab)  # Удаляем вкладку
                self.tab_counter -= 1  # Уменьшаем счетчик вкладок
                print(f"Удалена вкладка: {tab.text}, оставшиеся вкладки: {self.tab_counter}")  # Отладочное сообщение
                
                # Проверяем, нужно ли отключать кнопку удаления
                if self.tab_counter == 0:
                    self.del_tab_button.disabled = True
                    
                # Включаем кнопку добавления
                self.add_tab_button.disabled = False
                return  # Выходим из метода после удаления одной вкладки

        print("Нет вкладок для удаления, кроме 'Инфо'.")  # Отладочное сообщение


if __name__ == '__main__':
    MyApp().run()
