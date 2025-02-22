# ckicker
# загрузка в реп
git add .
git commit -m 'текст комментария'
git push

# Разработка
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt 

pyinstaller --onefile start.py


# что нужно
1. Горячие клавиши
2. Привязка к окну
3. Каждая вкладка автономна
4. Управление мышью
5. Запись макроса
6. Оптимизация
7. Внешний вид
8. *Доп. функции отслеживания изображения
9. *Статус бар на окне в таргете

# V 0.1
Окно вместе с консолью
Можно задавать задержку, указывать в скрипте одновременное нажатие клавиш, указывать паузы, краткое описание внутри, сохранение данных [Скачать](https://github.com/greyhayre/ckicker/releases/download/version/perfect_clicer.exe)