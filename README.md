Transactions csv

Описание проекта:

Консольное приложение для анализа финансовых транзакций из CSV-файлов. Позволяет группировать расходы по категориям и фильтровать их по дате. Результаты отправляются из апи в телеграмм чат пользователя. Приложение настроенно для асинхронной работы с большими файлами.

Используемые технологии:

 - FastAPI — для создания API.
 - Docker и Docker Compose — для контейнеризации приложения и удобства его запуска.
 - Aiogram - библиотека для создания бота.
 - Redis - как база данных.
 - Aiofiles - Для работы с большими файлами.


Требования:

Входные данные CSV-файл с колонками:

 - date (формат YYYY-MM-DD)
 - category (строка)
 - amount (число)
 - description (строка)

Пример строки:

2023-10-05,Food,15.50,Lunch

Функционал:

1. Парсинг CSV-файла.
2. Фильтрация транзакций по дате (если указаны --start_date и/или --end_date).
3. Группировка и подсчет суммы расходов по категориям.
4. Вывод результатов в консоль и чат телеграмм бота.

Обработка ошибок:

 - Некорректный формат файла
 - Некорректный формат дат
 - Отсутствие файла
 - Несоответствие колонок
 - Некорректное число amount
 - Возможность обработки любого порядка ввода данных в консоль

Аргументы командной строки:
Обязательный:

 - --file — путь к CSV-файлу

Опциональные:

 - --start_date — дата начала периода (формат YYYY-MM-DD) --end_date — дата конца периода (формат YYYY-MM-DD)

Запуск приложения:

Клонируйте репозиторий: git clone https://github.com/Oleg-Spider-Man/transactions_csv

Перейдите в директорию проекта: cd transactions_csv

Для запуска приложения нужно добавить в репозиторий проекта файл .env и заполнить его на основе файла .env.example в корне проекта. в DB_HOST_ нужно добавить хост вашего апи. в PORT_ нужно дабавить порт вашего апи.

Консольное приложение, апи и бота - нужно запустить в трех разных терминалах.

Команда запуска бота - python -m src.bot.bot_main
Команда запуска апи - uvicorn src.api.api_main:app --host 0.0.0.0 --port 8000 --reload
Пример команды запуска скрипта - python -m src.main --file src\test.csv --start_date 2023-10-01 --end_date 2023-10-03

Запустите с использованием Docker: Для запуска всех сервисов (Консольное приложение, приложение FastAPI, Бот Aiogram, Redis) выполните:

docker-compose up --build

Приложение будет доступно по адресу: http://localhost:8000/docs

Использование бота:

Для запуска бота нужно найти в телеграм, найти вашего бота по имени и отправить ему команду /start
