## О проекте
**`Foodgram`** — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также доступен сервис «Список покупок». Он позволяет создавать и скачивать (.txt) список продуктов, которые нужно купить для приготовления выбранных блюд.

![image](https://github.com/user-attachments/assets/f3a7ca77-99c7-4ac2-b81a-6906d9b5c16c)

Проект доступен по адресу https://foodgram-project.ddns.net

Ссылка на документацию с примерами запросов — https://foodgram-project.ddns.net/redoc/

## Установка и запуск
<details>
<summary>Инструкция по удаленному развертыванию</summary>

1. Форкнуть, клонировать репозиторий и перейти в корневую директорию проекта

```bash
git clone <ваша ссылка>
```

```bash
cd foodgram/
```

2. Создать .env файл в корневой директории по образцу

```env
# for settings.py

SECRET_KEY=Your secret key
DEBUG=True or any text for False
SERVER_IP=Your server ip
DOMAIN=Your domain

# for db

POSTGRES_DB=your_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

# for compose

USERNAME=Your username on DockerHub for images
GATEWAY_PORTS=Gateway ports
```

3. Добавить следующие секреты в настройкайх проекта на GitHub:
   - DOCKER_USERNAME — Ваш логин на DockerHub
   - DOCKER_PASSWORD — Ваш пароль на DockerHub
   - USER — Имя пользователя на удаленном сервере
   - HOST — IP-адрес вашего сервера
   - SSH_KEY — Закрытый SSH ключ для доступа к удаленному серверу
   - SSH_PASSPHRASE — Passphrase для закрытого ключа
   - TELEGRAM_TO — ID телеграм-аккаунта, на который будут приходить уведомления
   - TELEGRAM_TOKEN — Токен от вашего телеграм-бота, с которого планируете получать уведомления

> [!NOTE]
> Если не планируете получать уведомления в телеграм, то последние два секрета можно не добавлять, но в таком случае потребуется убрать блок send_message в файле .github/workflows/main.yml (строка 143).


4. Сбилдить и загрузить образы на DockerHub

```
cd frontend  # В директории frontend...
docker build -t username/foodgram_frontend .  # ...сбилдить образ, назвать его foodgram_frontend
cd ../backend  # То же в директории backend...
docker build -t username/foodgram_backend .
cd ../infra  # ...то же и в infra
docker build -t username/foodgram_gateway .
```

```
docker push username/foodgram_frontend
docker push username/foodgram_backend
docker push username/foodgram_gateway
```

5. Установка Docker на удаленный сервер

```bash
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin
```

6. Из корневой директории проекта выполните команду для копирования файлов на удаленный сервер или создайте файлы и перенесите скопированный код вручную

```bash
scp -i path_to_SSH/SSH_name docker-compose.production.yml \
    username@server_ip:/home/username/foodgram/docker-compose.production.yml

scp -i path_to_SSH/SSH_name .env \
    username@server_ip:/home/username/foodgram/.env
```

 - `path_to_SSH` — путь к файлу с SSH-ключом;
 - `SSH_name` — имя файла с SSH-ключом (без расширения);
 - `username` — ваше имя пользователя на сервере;
 - `server_ip` — IP вашего сервера.

7. Запустить docker-compose в режиме демона

```bash
sudo docker compose -f docker-compose.production.yml up -d
```

8. Выполнить миграции, собрать статику, заполнить бд подготовленными данными, создать суперпользователя

```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate

sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/docs/. /backend_static/static/redoc/

sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_tags_data
sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients_data

sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

9. Перенаправить все запросы в Docker

На сервере в редакторе nano откройте конфиг Nginx: `nano /etc/nginx/sites-enabled/default` и заполните его согласно примеру

```nano
server {
    server_name <# IP вашего сервера> <# Ваш доменный адрес>;

    location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:<# Порт, который вы указывали в GATEWAY_PORTS в файле .env>;
        client_max_body_size 20M;
    }

    # Здесь может быть различная техническая информация, например от Certbot

}

```

10. Автоматизация

Проект будет обновляться при выполнении команды `git push` из вашего локального репозитория, процесс вы сможете увидеть во вкладке Actions на GitHub.

</details>

<details>
<summary>Инструкция по локальному развертыванию</summary>

1. Форкнуть, клонировать репозиторий и перейти в корневую директорию проекта

```bash
git clone <ваша ссылка>
```

```bash
cd foodgram/
```

2. Создать .env файл в корневой директории по образцу

```env
# for settings.py

SECRET_KEY=Your secret key
DEBUG=True or any text for False
SERVER_IP=Your server ip
DOMAIN=Your domain

# for db

POSTGRES_DB=your_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

# for compose

USERNAME=Your username on DockerHub for images
GATEWAY_PORTS=Gateway ports
```

3. Запустить docker-compose

```bash
docker compose -f docker-compose.yml up --build
```

4. Выполнить миграции, собрать статику, заполнить бд подготовленными данными, создать суперпользователя

```bash
docker compose exec backend python manage.py migrate

docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
docker compose exec backend cp -r /app/docs/. /backend_static/static/redoc/

docker compose exec backend python manage.py load_tags_data
docker compose exec backend python manage.py load_ingredients_data

docker compose exec backend python manage.py createsuperuser
```

**Проект будет доступен по адресу 127.0.0.1:8080**

</details>

## Библиотеки `Python`

- `Django`==3.2.3
- `python-dotenv`==1.0.1
- `PyJWT`==2.9.0
- `Pillow`==9.3.0
- `gunicorn`==20.1.0
- `djoser`==2.1.0
- `djangorestframework`==3.12.4
- `djangorestframework-simplejwt`==4.7.2
- `django-filter`==23.1
- `django-cors-headers`==3.13.0
- `psycopg2-binary`==2.9.3

## Стек

`Python` `Django` `Django REST Framework (DRF)` `Gunicorn` `JavaScript` `React` `PostgeSQL` `Nginx` `Docker` `DockerHub` `CI/CD (GitHub Actions)`

#### Над бэкендом работал — [`wiacze`](https://github.com/wiacze)
