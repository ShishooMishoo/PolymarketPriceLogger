# GitHub - Быстрая шпаргалка

## 🚀 Первая загрузка (копируй-вставляй)

### 1. Откройте PowerShell в папке проекта
```powershell
cd C:\Poly\Price_logger
```

### 2. Выполните команды по порядку:

```bash
# Инициализация Git
git init

# Добавление всех файлов
git add .

# Создание коммита
git commit -m "Initial commit: Polymarket Price Monitor"

# Подключение к GitHub (ЗАМЕНИТЕ URL!)
git remote add origin https://github.com/ваш-username/ваш-репозиторий.git

# Переименование ветки в main
git branch -M main

# Отправка на GitHub
git push -u origin main
```

**При первом `git push` введите:**
- Username: ваш GitHub username
- Password: Personal Access Token (НЕ пароль от аккаунта!)

---

## 🔑 Создание Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token (classic)"
3. Название: `Polymarket Logger`
4. Поставить галочку: **`repo`**
5. Generate → Скопировать токен
6. Использовать вместо пароля

---

## 🔄 Обновление кода (после изменений)

```bash
# Проверить изменения
git status

# Добавить изменения
git add .

# Коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push
```

---

## 📋 Примеры сообщений коммита

```bash
git commit -m "Add new market to config"
git commit -m "Fix logging bug"
git commit -m "Update documentation"
git commit -m "Improve error handling"
git commit -m "Add health check endpoint"
```

---

## ⚠️ Частые ошибки

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/username/repo.git
```

### "Authentication failed"
Используйте Personal Access Token, НЕ пароль от GitHub

### "Author identity unknown"
```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

---

## 📱 Альтернатива: GitHub Desktop

Не хотите командную строку?

1. Скачайте [GitHub Desktop](https://desktop.github.com/)
2. File → Add local repository → `C:\Poly\Price_logger`
3. Commit → Push

---

## ✅ Проверка

После `git push` откройте:
```
https://github.com/ваш-username/ваш-репозиторий
```

Все файлы должны быть видны!

---

## 🚀 Деплой на Railway (после загрузки на GitHub)

1. [railway.app](https://railway.app) → Login with GitHub
2. New Project → Deploy from GitHub
3. Выберите репозиторий
4. Готово! Работает 24/7

---

**Подробная инструкция:** `GITHUB_GUIDE.md`
