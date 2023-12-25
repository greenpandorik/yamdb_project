![status workflow](https://github.com/greenpandorik/foodgram-project-react/actions/workflows/docker-image.yml/badge.svg)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

# Проект «Продуктовый помощник» - Foodgram

Foodgram - Продуктовый помощник. Сервис позволяет публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Requirements

Included in requirements.txt

```bash
pip install -r requirements.txt
```

## Run server

Run server using bash console

```bash
python manage.py runserver
```

## Deploy
**Установить Docker Compose на удалённом сервере:**
```
sudo apt-get update                                     - обновление пакетов актуальными версиями
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```
**Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra:**
```
scp docker-compose.yml nginx.conf username@IP:/home/username/
```

**Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения:**
```
SECRET_KEY              - секретный ключ Django проекта
DOCKER_PASSWORD         - пароль от Docker Hub
DOCKER_USERNAME         - логин Docker Hub
HOST                    - публичный IP сервера
USER                    - имя пользователя на сервере
PASSPHRASE              - *если ssh-ключ защищен паролем
SSH_KEY                 - приватный ssh-ключ

DB_ENGINE               - django.db.backends.postgresql
DB_NAME                 - postgres
POSTGRES_USER           - postgres
POSTGRES_PASSWORD       - postgres
DB_HOST                 - db
DB_PORT                 - 5432 (порт по умолчанию)
```

**Создать и запустить контейнеры Docker:**
```
 docker compose up -d --build
```
**Выполнить миграции, собрвть статику, импортировать ингредиенты:**
```
sudo docker compose exec web python manage.py migrate
sudo docker compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py import_ingredients_from_csv --path data/
```
**Создать суперпользователя:**
```
sudo docker compose exec web python manage.py createsuperuser
```
**Можно предыдущие два пункта сделать одной командой:**
```
sudo docker-compose exec web python manage.py collectstatic --noinput && sudo docker-compose exec web python manage.py migrate --noinput && sudo docker-compose exec web python manage.py import_ingredients_from_csv --path data/ && sudo docker-compose exec web python manage.py createsuperuser
```
**Остановка контейнеров и т.д. Docker:**
```
docker stop $(docker ps -qa) && docker rm $(docker ps -qa) && docker rmi -f $(docker images -qa) && docker volume rm $(docker volume ls -q) && docker network rm $(docker network ls -q)
```
### После каждого обновления репозитория (push в ветку master) будет происходить:

1. Проверка кода на соответствие стандарту PEP8 (flake8)
2. Сборка и доставка докер-образов на Docker Hub
3. Разворачивание проекта на удаленном сервере

### Развёртывание на локальном сервере

1. Выполните команду `docker-compose up -d --buld`.
2. Выполните миграции `docker-compose exec web python manage.py migrate`.
3. Создайте суперюзера `docker-compose exec web python manage.py createsuperuser`.
4. Соберите статику `docker-compose exec web python manage.py collectstatic --no-input`.
5. Заполните базу ингредиентами 
`docker-compose exec web python manage.py import_ingredients_from_file_csv --path data/ingredients.csv`. 
5. Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>.


# Автор:
   <img src="https://media.giphy.com/media/WUlplcMpOCEmTGBtBW/giphy.gif" width="30">
   Михаил Волков - green_panda@inbox.ru
