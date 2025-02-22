import win32gui
import pyautogui
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

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
        self.target_button = target_button

        layout = BoxLayout(orientation='vertical')

        try:
            window_titles = get_window_titles()
            if not window_titles:
                layout.add_widget(Label(text="Нет открытых окон."))
            else:
                for window in window_titles:
                    if window:
                        button = Button(text=window)
                        button.bind(on_release=self.select_window)
                        layout.add_widget(button)
        except Exception as e:
            layout.add_widget(Label(text=f"Ошибка: {e}"))

        self.content = layout

    def select_window(self, instance):
        selected_window = instance.text
        self.target_button.text = selected_window
        self.dismiss()

class TabContent(TabbedPanelItem):
    def __init__(self, title, key_presses, **kwargs):
        super(TabContent, self).__init__(**kwargs)
        self.text = title
        self.key_presses = key_presses
        self.selected_window = None

        layout = BoxLayout(orientation='vertical')
        self.target_button = Button(text="Выберите окно")
        self.target_button.bind(on_release=self.open_window_selector)

        self.send_button = Button(text="Отправить нажатия")
        self.send_button.bind(on_release=self.send_key_presses)
        self.send_button.disabled = True  # Изначально кнопка отключена

        layout.add_widget(self.target_button)
        layout.add_widget(self.send_button)
        self.add_widget(layout)

    def open_window_selector(self, instance):
        window_selector = WindowSelector(target_button=self.target_button)
        window_selector.bind(on_dismiss=self.set_selected_window)
        window_selector.open()

    def set_selected_window(self, instance):
        self.selected_window = self.target_button.text
        self.send_button.disabled = False  # Включаем кнопку отправки, если окно выбрано

    def send_key_presses(self, instance):
        if self.selected_window:
            hwnd = win32gui.FindWindow(None, self.selected_window)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                for key in self.key_presses:
                    if isinstance(key, str):
                        pyautogui.press(key)
                    elif isinstance(key, tuple):
                        pyautogui.hotkey(*key)
            else:
                error_popup = Popup(title="Ошибка", content=Label(text="Не удалось найти выбранное окно."), size_hint=(0.5, 0.5))
                error_popup.open()

class MyApp(App):
    def build(self):
        tab_panel = TabbedPanel()

        # Создание вкладок с различными нажатиями клавиш
        tab1 = TabContent(title='Tab 1', key_presses=["h", "e", "l", "l", "o", "enter"])
        tab2 = TabContent(title='Tab 2', key_presses=["w", "o", "r", "l", "d", "enter", ("ctrl", "s")])

        tab_panel.add_widget(tab1)
        tab_panel.add_widget(tab2)

        return tab_panel

if __name__ == '__main__':
    MyApp().run()


