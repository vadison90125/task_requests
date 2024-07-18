# Test Requests
![Crates.io](https://img.shields.io/badge/Python-Pytest-yellow)
![Crates.io](https://img.shields.io/badge/Allure-8A2BE2)

Базовый url - https://jsonplaceholder.typicode.com

* GET - /posts
* POST  - /posts
* PUT -  /posts
* DELETE - /posts

Документация - https://jsonplaceholder.typicode.com/guide

Задание:

- Покрыть эндпоинты тестами, используя Pytest и Allure

# Установка Allure

В терминале PowerShell выполнить команды:
```sh
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
```sh
irm get.scoop.sh | iex
```
```sh
scoop install allure
```
# Установка модулей

В корне проекта (в созданном окружении) выполнить команду:
```sh
pip install -r requirements.txt
```
#### Запуск тестов:
Из директории /task_requests/tests/ выполнить команду:
```sh
pytest --alluredir=../tests/allure-reports
```
#### Просмотр отчёта:
Из директории /task_requests/tests/ выполнить команду:
```sh
allure serve allure-reports
```
