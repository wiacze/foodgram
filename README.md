## О проекте
**Foodgram** — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также доступен сервис «Список покупок». Он позволяет создавать и скачивать (.txt) список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект доступен по адресу https://foodgram-project.ddns.net

Ссылка на документацию с примерами запросов — https://foodgram-project.ddns.net/redoc/

## Установка и запуск
<details>
<summary>Инструкция</summary>

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


. Запустить docker-compose

```bash
docker compose -f docker-compose.production.yml up -d
```

. Выполнить миграции, собрать статику и заполнить бд подготовленными данными

```
Для выполнения команд могут потребоваться права администратора, в таком случае достаточно перед каждой командой прописать sudo
```

```bash
docker compose -f docker-compose.production.yml exec backend python manage.py migrate

docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
docker compose -f docker-compose.production.yml exec backend cp -r /app/docs/. /backend_static/static/redoc/

docker compose -f docker-compose.production.yml exec backend python manage.py load_tags_data
docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients_data
```


</details>

2. Необходимые инструменты
3. Инструкция по установке и запуску
5. Стек технологий
6. Автор
