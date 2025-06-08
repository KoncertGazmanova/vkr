@echo off
REM Запуск сервера Django
start cmd /k "python manage.py runserver"
REM Запуск фронтенда React
cd frontend && start cmd /k "npm start"
