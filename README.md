# Library Management System - REST API
## Описание проекта
REST API для управления библиотекой, реализованное на Django и Django REST Framework. Система предоставляет функционал для управления книгами, авторами, пользователями и отслеживания выдачи книг.
## Основные возможности
### 📚 Управление книгами и авторами

### 👥 Аутентификация пользователей через JWT

### 🔒 Ролевая модель доступа (администраторы, модераторы, читатели)

### 📅 Система учета выдачи книг

### 📊 Автоматическая документация API (OpenAPI/Swagger)

## 🚀 Функциональность
## Основная часть (обязательная по ТЗ):
#### ✅ CRUD для клиентов 
#### ✅ CRUD для книг
#### ✅ CRUD для авторов
#### ✅ Регистрация и аутентификация пользователей (через email)
#### ✅ Ограничение доступа: пользователь видит только свои данные, изменять авторов и книг может только создатель или модератор
#### ✅ Роли:неавторизованные пользователи, модераторы и владельцы книг и авторов
#### ✅ CRUD операции описаны через Generic классы
#### ✅ Описаны сериализаторы для каждой модели
#### ✅ Создана автоматическая документация API (OpenAPI/Swagger)
#### ✅ Реализована сборка и установка образов через Docker-compose
#### ✅ Реализован workflow через CI/CD

### Дополнительная часть (расширение функциональности):

#### ✅ Описана пагинация 
#### ✅ Созданы валидаторы
#### ✅ Написаны тесты через unittest
#### ✅ Создана периодическая задача для отправки уведомлений на почту

## Технологический стек
#### Backend: Django 4.2 + Django REST Framework

#### База данных: PostgreSQL

#### Аутентификация: JWT (Simple JWT)

#### Контейнеризация: Docker + Docker Compose

#### Документация: DRF Spectacular (OpenAPI 3.0)

## 📂 Установка и запуск
### Установка Docker и Docker Compose
Обновление пакетов:
```
sudo apt update
```
установка Docker:
```
sudo apt install docker-compose
```
###  Настройка SSH-доступа
Сгенерируйте SSH-ключ на локальной машине:
```
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N ""
```
Скопируйте публичный ключ на сервер:
```
ssh-copy-id -i ~/.ssh/deploy_key.pub ваш_пользователь@ip_сервера
```
Проверьте подключение:
```
ssh -i ~/.ssh/deploy_key ваш_пользователь@ip_сервера
```

### Подготовка GitHub Secrets
В настройках репозитория GitHub:

Перейдите в Settings → Secrets and variables → Actions

Создайте новые секреты:

DOCKER_HUB_USERNAME - ваш логин на Docker Hub

DOCKER_HUB_ACCESS_TOKEN - токен доступа Docker Hub

SSH_PRIVATE_KEY - содержимое файла deploy_key (приватный ключ)

SSH_USER - пользователь сервера (например, ubuntu)

SERVER_IP - IP-адрес вашего сервера

Клонировать репозиторий:
```
 git clone https://github.com/yourname/Library_management.git`
cd Library_management
```

Создать и активировать виртуальное окружение:
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
Создать файл .env на основе .env.example:
```
cp .env.example .env
```
Запустить сервисы:
```
docker-compose up -d --build
```

Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Либо воспользоваться кастомной командой:
```
docker-compose exec web python manage.py csu
```
 ### Workflow CI/CD
При каждом пуше в ветку develop автоматически выполняются:

1. Линтинг кода (Flake8)

2. Запуск тестов (pytest)

3. Сборка Docker-образа и публикация в Docker Hub

4. Деплой на удалённый сервер

## Доступ к сервисам
### API: http://localhost:8000/api/

### Админка: http://localhost:8000/admin/

## Документация API:

### Swagger UI: http://localhost:8000/api/schema/swagger-ui/

### ReDoc: http://localhost:8000/api/schema/redoc/

### Мой адрес сервера
```
ssh -l kovaleva121 158.160.173.120
```