import win32gui
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

def get_window_titles():
    titles = []
    def enum_window_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            titles.append(win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(enum_window_callback, None)
    return titles

class WindowSelector(Popup):
    def __init__(self, target_button, **kwargs):
        super(WindowSelector, self).__init__(**kwargs)
        self.title = "Выберите окно"
        self.size_hint = (0.8, 0.8)
        self.target_button = target_button  # Сохраняем ссылку на кнопку

        layout = BoxLayout(orientation='vertical')

        try:
            # Получаем список всех открытых окон
            window_titles = get_window_titles()
            print(window_titles)  # Выводим заголовки окон в консоль
            
            if not window_titles:
                layout.add_widget(Label(text="Нет открытых окон."))
            else:
                for window in window_titles:
                    if window:  # Проверяем, что заголовок окна не пустой
                        button = Button(text=window)
                        button.bind(on_release=self.select_window)
                        layout.add_widget(button)
        except Exception as e:
            layout.add_widget(Label(text=f"Ошибка: {e}"))

        self.content = layout

    def select_window(self, instance):
        selected_window = instance.text
        print(f"Выбрано окно: {selected_window}")
        self.target_button.text = selected_window  # Изменяем текст кнопки таргета
        self.dismiss()  # Закрываем окно выбора