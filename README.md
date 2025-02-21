# ckicker
# загрузка в реп
git add .
git commit -m 'текст комментария'
git push

# Разработка
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt 

# что нужно
1. Интерфейс - kivi  https://kivy.org/
2. Эмуляция клавиатуры - pyautogui https://pyautogui.readthedocs.io/en/latest/
4. Созранение данных перед выходом - json
5. привязка к окну - win32gui
6. задача под звездочкой комп зрение и запись макросов в реальном времени - ?

# V 0.1
Окно вместе с консолью
Можно задавать задержку, указывать в скрипте одновременное нажатие клавиш, указывать паузы, краткое описание внутри, сохранение данных