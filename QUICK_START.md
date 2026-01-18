# Quick Start Guide - 5 Minutes to Launch

## ✅ Readiness Checklist

- [ ] Python 3.7+ installed
- [ ] Internet connection active
- [ ] All project files downloaded

## 🚀 Launch in 3 Steps

### Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

### Step 2: Configure Markets (2 minutes)

Open `config.json` and add your markets:

```json
{
  "markets": [
    {
      "slug": "your-market-slug",
      "name": "Market Name",
      "enabled": true
    }
  ],
  "settings": {
    "poll_interval_seconds": 60,
    "config_reload_interval_seconds": 30,
    "output_directory": "logs"
  }
}
```

**How to find the slug?**
1. Open the market on polymarket.com
2. Click on a specific question
3. Copy the last part of the URL after the final `/`

**Example:**
- URL: `https://polymarket.com/event/portugal-presidential-election/will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`
- Slug: `will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`

### Step 3: Launch (10 seconds)

**Windows:**
```bash
start_service.bat
```

**Linux/Mac:**
```bash
python price_monitor_service.py
```

## ✨ Done!

Service is running! You will see:

```
============================================================
Polymarket Price Monitor Service
============================================================

Starting monitor: Portugal Election - João Cotrim Figueiredo
[Portugal Election] Initialization complete
[Portugal Election] Starting monitoring...

Monitors running: 1
Log directory: logs
Poll interval: 60 seconds

Press Ctrl+C to stop
============================================================

[Portugal Election] [2026-01-18 12:30:00] Entry #1: Bid=0.162, Ask=0.164, Mid=0.163
```

## 📊 Data Verification

Data is saved in the `logs/` directory:

```bash
ls logs/
# output: market-slug_2026-01-18.json
```

Sample content:
```json
[
  {
    "timestamp": "2026-01-18T12:30:00",
    "market_name": "Will João Cotrim Figueiredo win...",
    "bid": 0.162,
    "ask": 0.164,
    "mid": 0.163
  }
]
```

## 🔄 Adding New Markets (Without Stopping!)

1. Open `config.json`
2. Add a new market to the `markets` array:
   ```json
   {
     "slug": "new-market-slug",
     "name": "New Name",
     "enabled": true
   }
   ```
3. Save the file
4. After 30 seconds, the service will automatically start monitoring the new market!

## ⏸️ Stopping

Press `Ctrl+C` in the console where the service is running.

## ❓ Something Not Working?

### Problem: "requests module not found"
**Solution:**
```bash
pip install requests
```

### Problem: "Error: market not found"
**Solution:** Check the slug correctness in config.json

### Problem: Garbled text instead of readable output (Windows)
**Solution:** Already fixed in code! If still seeing issues, run:
```bash
chcp 65001
```

### Problem: Service won't start
**Solution:**
1. Check JSON syntax in config.json (use jsonlint.com)
2. Ensure Python 3.7+: `python --version`
3. Check console logs

## 📖 Further Learning

- **Detailed documentation:** `SERVICE_GUIDE.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`
- **Architecture:** `PROJECT_STRUCTURE.md`
- **Full overview:** `SUMMARY.md`

## 💡 Useful Tips

### Run in Background (Linux/Mac)
```bash
nohup python price_monitor_service.py > service.log 2>&1 &
```

### View Logs in Real-Time
```bash
tail -f logs/market-slug_$(date +%Y-%m-%d).json
```

### Check if Service is Running
```bash
ls -lh logs/
# should see fresh files with today's date
```

### Data Backup
```bash
# Windows
xcopy logs logs_backup\ /E /I /Y

# Linux/Mac
cp -r logs logs_backup
```

## 🎯 Typical Configurations

### 1. Single Market, Every Minute
```json
{
  "markets": [{"slug": "your-slug", "name": "Market", "enabled": true}],
  "settings": {"poll_interval_seconds": 60, "output_directory": "logs"}
}
```

### 2. Multiple Markets, Every 2 Minutes
```json
{
  "markets": [
    {"slug": "market-1", "name": "Market 1", "enabled": true},
    {"slug": "market-2", "name": "Market 2", "enabled": true},
    {"slug": "market-3", "name": "Market 3", "enabled": true}
  ],
  "settings": {"poll_interval_seconds": 120, "output_directory": "logs"}
}
```

### 3. High Frequency (30 sec)
```json
{
  "markets": [{"slug": "your-slug", "name": "HF Market", "enabled": true}],
  "settings": {"poll_interval_seconds": 30, "output_directory": "hf_logs"}
}
```

## ✅ Successful Launch Checklist

- [x] Dependencies installed
- [x] config.json configured
- [x] Service started
- [x] Logs visible in console
- [x] logs/ directory created
- [x] Data files being created
- [x] Entries added every minute

**If all items are checked - everything is working great!** 🎉

---

**Setup Time:** 5 minutes
**Difficulty:** 🟢 Easy
**Status:** Ready to use
