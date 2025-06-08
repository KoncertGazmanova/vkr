@echo off
REM Остановка всех процессов сервера и фронтенда
REM Закрытие всех окон командной строки
for /f "tokens=2" %%i in ('tasklist ^| findstr cmd.exe') do taskkill /pid %%i /f
