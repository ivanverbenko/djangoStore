# djangoStore
Проект магазина на Django

### Стек
Posgre
Django
Redis

### Запуск проекта

#### Установка зависимостей
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Запуск celery
```bash
celery -A store worker --loglevel=INFO
```
#### Запуск проекта
```bash
./manage.py migrate
./manage.py runserver 
```
