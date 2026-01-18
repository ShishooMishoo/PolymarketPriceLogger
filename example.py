"""
Пример использования Polymarket Price Logger
"""
from polymarket_price_logger import log_market_prices

# Пример: Portugal Presidential Election - João Cotrim Figueiredo
# Используйте slug рынка (можно скопировать из URL на polymarket.com)
MARKET_ID = "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643"

# Мониторинг в течение 60 минут
log_market_prices(
    market_id=MARKET_ID,
    duration_minutes=60,
    log_file="portugal_election_prices.json"
)

# Для бесконечного мониторинга раскомментируйте:
# log_market_prices(
#     market_id=MARKET_ID,
#     duration_minutes=None,
#     log_file="portugal_election_prices.json"
# )
