"""
Запуск мониторинга цен для Portugal Presidential Election
"""
from polymarket_price_logger import log_market_prices

# Portugal Presidential Election - João Cotrim Figueiredo
MARKET_SLUG = "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643"

if __name__ == "__main__":
    print("=" * 60)
    print("Polymarket Price Logger")
    print("Рынок: Portugal Presidential Election - João Cotrim Figueiredo")
    print("=" * 60)
    print()

    log_market_prices(
        market_id=MARKET_SLUG,
        duration_minutes=None,  # Бесконечный мониторинг
        log_file="portugal_election_prices.json"
    )
