@echo off
chcp 65001 >nul
echo ========================================
echo GitHub Upload Script
echo ========================================
echo.

REM Проверка наличия Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git не установлен!
    echo Скачайте с: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/6] Проверка Git конфигурации...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo [!] Git не настроен. Настройте:
    echo     git config --global user.name "Your Name"
    echo     git config --global user.email "your@email.com"
    pause
    exit /b 1
)

echo [2/6] Инициализация Git...
if not exist ".git" (
    git init
    echo Git репозиторий инициализирован
) else (
    echo Git репозиторий уже существует
)

echo [3/6] Добавление файлов...
git add .
echo Файлы добавлены

echo [4/6] Создание коммита...
set /p COMMIT_MSG="Введите сообщение коммита (или Enter для 'Update'): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update

git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [!] Нет изменений для коммита или произошла ошибка
)

echo [5/6] Проверка remote...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [!] Remote 'origin' не настроен
    set /p REPO_URL="Введите URL репозитория (https://github.com/username/repo.git): "
    git remote add origin !REPO_URL!
    echo Remote добавлен
) else (
    echo Remote уже настроен
)

echo [6/6] Отправка на GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Не удалось отправить на GitHub
    echo.
    echo Возможные причины:
    echo 1. Неправильный URL репозитория
    echo 2. Нет прав доступа (нужен Personal Access Token)
    echo 3. Нет интернет-соединения
    echo.
    echo Создайте Personal Access Token:
    echo GitHub Settings -^> Developer settings -^> Personal access tokens -^> Generate
    echo Используйте токен вместо пароля при git push
) else (
    echo.
    echo ========================================
    echo [SUCCESS] Загрузка завершена!
    echo ========================================
    echo.
    echo Ваш код на GitHub!
    echo Проверьте: https://github.com/your-username/your-repo
)

echo.
pause
