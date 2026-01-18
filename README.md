# Polymarket Price Logger

Tools for monitoring and logging bid/ask prices on Polymarket markets.

## Two Operating Modes

### 1. Simple Script (polymarket_price_logger.py)
Monitor a single market for a specified duration.

### 2. Service (price_monitor_service.py) ⭐ Recommended
Continuous monitoring of multiple markets with hot configuration reload.

---

## Service Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
Edit `config.json`:
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

### 3. Launch
**Windows:**
```bash
start_service.bat
```

**Linux/Mac:**
```bash
python price_monitor_service.py
```

📖 **Detailed documentation:** [SERVICE_GUIDE.md](SERVICE_GUIDE.md)

---

## 📤 Upload to GitHub

Before deploying to the cloud, upload the project to GitHub:

### Automatic method:
1. Create a repository at [github.com/new](https://github.com/new)
2. Run: **`upload_to_github.bat`**
3. Follow the on-screen instructions

### Manual method:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

📖 **Instructions:**
- **Quick reference:** [GITHUB_QUICK.md](GITHUB_QUICK.md) - 5 commands
- **Detailed guide:** [GITHUB_GUIDE.md](GITHUB_GUIDE.md) - all details

---

## ☁️ Cloud Deployment

After uploading to GitHub, deploy to the cloud in 5 minutes!

### Quick options:

| Platform | Price | Setup Time | Link |
|----------|-------|------------|------|
| **Railway** | $5/mo | 5 minutes | [railway.app](https://railway.app) |
| **Oracle Cloud** | **Free!** | 20 minutes | [oracle.com/cloud/free](https://oracle.com/cloud/free) |
| **DigitalOcean** | $4/mo | 15 minutes | [digitalocean.com](https://digitalocean.com) |

📖 **Deployment instructions:**
- **Quick start:** [DEPLOY_QUICK.md](DEPLOY_QUICK.md) (3 simple options)
- **Complete guide:** [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) (all platforms)

---

## Using the Simple Script

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from polymarket_price_logger import log_market_prices

# Monitor market for 60 minutes
log_market_prices(
    market_id="will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643",
    duration_minutes=60,
    log_file="prices.json"
)
```

### Parameters

- `market_id` (str): Polymarket market slug
- `duration_minutes` (int, optional): Monitoring duration in minutes. `None` = infinite
- `log_file` (str): JSON file name for saving data

### How to Find market_id (slug)

1. Open the market on polymarket.com
2. URL will look like: `https://polymarket.com/event/portugal-presidential-election`
3. Click on a specific question (e.g., "Will João Cotrim Figueiredo win?")
4. URL will change to: `https://polymarket.com/event/portugal-presidential-election/will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`
5. Copy the last part after the final `/` - this is the slug: `will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`

### Data Format

```json
[
  {
    "timestamp": "2026-01-18T12:30:00",
    "market_id": "0x1234...",
    "market_name": "Will Trump win 2024?",
    "token_id": "12345",
    "bid": 0.52,
    "ask": 0.54,
    "mid": 0.53
  }
]
```

## Examples

### Monitor for 1 hour
```bash
python example.py
```

### Infinite monitoring
Change `duration_minutes=None` in example.py and stop with Ctrl+C

## API Endpoints

- Gamma API: `https://gamma-api.polymarket.com`
- CLOB API: `https://clob.polymarket.com`
