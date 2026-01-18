# GitHub - Quick Reference

## 🚀 First Upload (Copy-Paste)

### 1. Open PowerShell in Project Folder
```powershell
cd C:\Poly\Price_logger
```

### 2. Execute Commands in Order:

```bash
# Initialize Git
git init

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Polymarket Price Monitor"

# Connect to GitHub (REPLACE URL!)
git remote add origin https://github.com/your-username/your-repository.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**On first `git push` enter:**
- Username: your GitHub username
- Password: Personal Access Token (NOT account password!)

---

## 🔑 Creating Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token (classic)"
3. Name: `Polymarket Logger`
4. Check: **`repo`**
5. Generate → Copy token
6. Use instead of password

---

## 🔄 Updating Code (After Changes)

```bash
# Check changes
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push
```

---

## 📋 Commit Message Examples

```bash
git commit -m "Add new market to config"
git commit -m "Fix logging bug"
git commit -m "Update documentation"
git commit -m "Improve error handling"
git commit -m "Add health check endpoint"
```

---

## ⚠️ Common Errors

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/username/repo.git
```

### "Authentication failed"
Use Personal Access Token, NOT GitHub password

### "Author identity unknown"
```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

---

## 📱 Alternative: GitHub Desktop

Don't want command line?

1. Download [GitHub Desktop](https://desktop.github.com/)
2. File → Add local repository → `C:\Poly\Price_logger`
3. Commit → Push

---

## ✅ Verification

After `git push` open:
```
https://github.com/your-username/your-repository
```

All files should be visible!

---

## 🚀 Deploy to Railway (After GitHub Upload)

1. [railway.app](https://railway.app) → Login with GitHub
2. New Project → Deploy from GitHub
3. Select repository
4. Done! Running 24/7

---

**Detailed guide:** `GITHUB_GUIDE.md`
