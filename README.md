Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/andrey-ushak0v/hw05_final.git
cd api_final_yatube
Cоздать и активировать виртуальное окружение:

python3 -m venv venv
source venv/bin/activate
Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip
pip install -r requirements.txt
Выполнить миграции:

python3 manage.py migrate
Запустить проект:

python3 manage.py runserver

Описание проекта:

этот учебный проект разрабатывался в учебных целях студентом Яндекс-практикума
представляет собой небольшой блог, в котором можно создать публикацию, закрепить ее в группе, а так же подписаться на люыимых авторов

технологии:

Python, Django
