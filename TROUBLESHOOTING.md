# Troubleshooting - Polymarket Price Logger

Document describing problems encountered during development and their solutions.

---

## Problem 1: API 422 Error When Requesting Market Details

### Symptoms
```
API Error: 422
Error: failed to get data for market 0xe90b27f08082e17740308fdc957528d29a3f334a9ecaeefd056a3427a4cfdaaf
```

### Cause
Gamma API doesn't accept `condition_id` in URL path format (`/markets/{condition_id}`). API expects parameters via query string.

### Solution
Change request method from:
```python
url = f"{GAMMA_API_BASE}/markets/{market_id}"
response = requests.get(url, timeout=10)
```

To:
```python
url = f"{GAMMA_API_BASE}/markets"
params = {"slug": market_id}
response = requests.get(url, params=params, timeout=10)
```

**Important:** Use `slug` instead of `condition_id` to get market information.

---

## Problem 2: Incorrect Filtering by condition_id

### Symptoms
When requesting with `condition_id` parameter, API returns wrong markets (e.g., old 2020 markets instead of Portugal Presidential Election 2026).

### Cause
The `condition_id` parameter in Gamma API works incorrectly and returns arbitrary markets instead of filtering by specific condition_id.

### Solution
Use `slug` parameter instead of `condition_id`:
```python
params = {"slug": "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643"}
```

**How to find slug:**
1. Open market on polymarket.com
2. URL: `https://polymarket.com/event/portugal-presidential-election/will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`
3. Slug is the last part of URL after `/`

---

## Problem 3: API 400 Error When Requesting Prices

### Symptoms
```
Price API Error: 400
Error: failed to get prices for token 28238304963115391468520084611709080022027216241044579007402765414035709535435
```

### Cause
CLOB API endpoint `/price` requires mandatory `side` parameter (buy or sell), but this parameter wasn't passed in the code.

API response when parameter is missing:
```json
{"error": "Invalid side"}
```

### Solution
Need to make two separate requests to get bid and ask:

```python
# Get bid (buy price)
response_buy = requests.get(url, params={"token_id": token_id, "side": "buy"}, timeout=10)

# Get ask (sell price)
response_sell = requests.get(url, params={"token_id": token_id, "side": "sell"}, timeout=10)
```

Then extract prices from responses:
```python
bid = float(bid_data.get('price', 0)) if bid_data.get('price') else None
ask = float(ask_data.get('price', 0)) if ask_data.get('price') else None
mid = (bid + ask) / 2 if bid and ask else None
```

**Important:**
- `side=buy` returns buy price (bid)
- `side=sell` returns sell price (ask)
- `mid` is calculated as average of bid and ask

---

## Problem 4: UnicodeEncodeError in Windows Console

### Symptoms
```
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-6: character maps to <undefined>
```

Occurs when outputting Russian text or special characters (e.g., "João").

### Cause
By default, Windows console uses cp1252 encoding, which doesn't support Cyrillic and many special characters.

### Solution
Reconfigure stdout to UTF-8 at the beginning of function:

```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

This needs to be done before any console output containing non-ASCII characters.

---

## Problem 5: Incorrect clobTokenIds Data Structure

### Symptoms
Unable to extract token_id from API response.

### Cause
The `clobTokenIds` field in API response can be either a JSON string or an already parsed array, depending on API version or request type.

### Solution
Check data type and parse if necessary:

```python
clob_token_ids = market_details.get('clobTokenIds')
token_ids = json.loads(clob_token_ids) if isinstance(clob_token_ids, str) else clob_token_ids

# Take first token (YES)
token_id = token_ids[0] if isinstance(token_ids, list) and len(token_ids) > 0 else None
```

**Important:** First token in array is always "YES" token, second is "NO".

---

## Problem 6: Missing Tokens in Old API Format

### Symptoms
```
Error: market contains no tokens
```

### Cause
Old markets used `tokens` field instead of `clobTokenIds`. New markets only use `clobTokenIds`.

### Solution
Use only `clobTokenIds` for all modern markets:

```python
clob_token_ids = market_details.get('clobTokenIds')
if not clob_token_ids:
    print("Error: market contains no tokens")
    return None
```

Don't try to use `tokens` field - it's deprecated format.

---

## General Recommendations

### API Endpoints
- **Gamma API:** `https://gamma-api.polymarket.com` - for getting market information
- **CLOB API:** `https://clob.polymarket.com` - for getting prices

### Request Structure

1. **Get market information:**
   ```
   GET https://gamma-api.polymarket.com/markets?slug={market_slug}
   ```

2. **Get bid price:**
   ```
   GET https://clob.polymarket.com/price?token_id={token_id}&side=buy
   ```

3. **Get ask price:**
   ```
   GET https://clob.polymarket.com/price?token_id={token_id}&side=sell
   ```

### Timeouts
Always set timeout for HTTP requests (recommended 10 seconds):
```python
response = requests.get(url, params=params, timeout=10)
```

### Error Handling
Always check:
1. HTTP status code (200 = success)
2. Presence of data in response
3. Correctness of data structure

### File Encoding
When working with JSON files always specify UTF-8:
```python
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

Parameter `ensure_ascii=False` is important for correct saving of non-ASCII characters (Cyrillic, special characters).

---

## Useful Debugging Commands

### Testing API via curl

```bash
# Get market information
curl "https://gamma-api.polymarket.com/markets?slug=will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643"

# Get bid price
curl "https://clob.polymarket.com/price?token_id=28238304963115391468520084611709080022027216241044579007402765414035709535435&side=buy"

# Get ask price
curl "https://clob.polymarket.com/price?token_id=28238304963115391468520084611709080022027216241044579007402765414035709535435&side=sell"
```

### Testing Individual Functions

```python
from polymarket_price_logger import get_market_details, get_current_price

# Test getting market details
market = get_market_details("will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643")
print(market['question'])
print(market['clobTokenIds'])

# Test getting prices
token_id = "28238304963115391468520084611709080022027216241044579007402765414035709535435"
prices = get_current_price(token_id)
print(prices)
```

---

## Change History

**2026-01-18:** Document created based on problems encountered during Price Logger development for Portugal Presidential Election.
