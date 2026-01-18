import time
import json
from datetime import datetime
import os
import requests


# API endpoints
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"


def log_market_prices(market_id: str, duration_minutes: int = None, log_file: str = "price_log.json"):
    """
    Мониторит указанный рынок Polymarket и записывает лучшие bid/ask цены каждую минуту.

    Args:
        market_id: ID рынка Polymarket для мониторинга
        duration_minutes: Длительность мониторинга в минутах (None = бесконечно)
        log_file: Имя файла для записи логов
    """
    # Настраиваем кодировку для Windows консоли
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print(f"Начинаю мониторинг рынка {market_id}")
    print(f"Данные будут записываться в {log_file}")

    # Создаем файл, если его нет
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

    start_time = time.time()
    iteration = 0

    try:
        while True:
            # Проверяем, не истекло ли время
            if duration_minutes is not None:
                elapsed_minutes = (time.time() - start_time) / 60
                if elapsed_minutes >= duration_minutes:
                    print(f"\nМониторинг завершен ({duration_minutes} минут)")
                    break

            try:
                # Получаем детали рынка
                market_details = get_market_details(market_id)

                if not market_details:
                    print(f"Ошибка: не удалось получить данные для рынка {market_id}")
                    time.sleep(60)
                    continue

                # Получаем token_id для YES токена из clobTokenIds
                clob_token_ids = market_details.get('clobTokenIds')
                if not clob_token_ids:
                    print("Ошибка: рынок не содержит токенов")
                    time.sleep(60)
                    continue

                # clobTokenIds - это JSON строка, парсим её
                import json as json_module
                token_ids = json_module.loads(clob_token_ids) if isinstance(clob_token_ids, str) else clob_token_ids

                # Берем первый токен (YES)
                token_id = token_ids[0] if isinstance(token_ids, list) and len(token_ids) > 0 else None

                if not token_id:
                    print("Ошибка: не удалось извлечь token_id")
                    time.sleep(60)
                    continue

                market_name = market_details.get('question', 'Unknown')

                # Получаем текущие цены
                price_data = get_current_price(token_id)

                if not price_data:
                    print(f"Ошибка: не удалось получить цены для токена {token_id}")
                    time.sleep(60)
                    continue

                # Формируем запись
                timestamp = datetime.now().isoformat()
                log_entry = {
                    "timestamp": timestamp,
                    "market_id": market_id,
                    "market_name": market_name,
                    "token_id": token_id,
                    "bid": price_data.get('bid'),
                    "ask": price_data.get('ask'),
                    "mid": price_data.get('mid')
                }

                # Читаем существующие данные
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)

                # Добавляем новую запись
                logs.append(log_entry)

                # Записываем обратно в файл
                with open(log_file, 'w', encoding='utf-8') as f:
                    json.dump(logs, f, indent=2, ensure_ascii=False)

                iteration += 1
                print(f"[{timestamp}] Итерация {iteration}: Bid={log_entry['bid']}, Ask={log_entry['ask']}, Mid={log_entry['mid']}")

            except Exception as e:
                print(f"Ошибка при получении данных: {e}")

            # Ждем 60 секунд до следующей итерации
            time.sleep(60)

    except KeyboardInterrupt:
        print(f"\nМониторинг остановлен пользователем")
        print(f"Записано {iteration} записей в {log_file}")


def get_market_details(market_id: str):
    """
    Получает детали рынка через Gamma API.

    Args:
        market_id: Slug рынка (например, "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643")

    Returns:
        dict: Данные рынка или None при ошибке
    """
    try:
        # Получаем по slug
        url = f"{GAMMA_API_BASE}/markets"
        params = {"slug": market_id}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # API возвращает массив, берем первый элемент
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            print("Ошибка: рынок не найден")
            return None
        else:
            print(f"Ошибка API: {response.status_code}")
            return None

    except Exception as e:
        print(f"Ошибка при получении деталей рынка: {e}")
        return None


def get_current_price(token_id: str):
    """
    Получает текущие цены для токена через CLOB API.

    Args:
        token_id: ID токена

    Returns:
        dict: Данные цен (bid, ask, mid) или None при ошибке
    """
    try:
        url = f"{CLOB_API_BASE}/price"

        # Получаем bid (цена покупки)
        response_buy = requests.get(url, params={"token_id": token_id, "side": "buy"}, timeout=10)
        # Получаем ask (цена продажи)
        response_sell = requests.get(url, params={"token_id": token_id, "side": "sell"}, timeout=10)

        if response_buy.status_code == 200 and response_sell.status_code == 200:
            bid_data = response_buy.json()
            ask_data = response_sell.json()

            # Получаем цены
            bid = float(bid_data.get('price', 0)) if bid_data.get('price') else None
            ask = float(ask_data.get('price', 0)) if ask_data.get('price') else None

            # Вычисляем mid
            mid = None
            if bid is not None and ask is not None:
                mid = (bid + ask) / 2

            return {
                'bid': bid,
                'ask': ask,
                'mid': mid
            }
        else:
            print(f"Ошибка API цен: buy={response_buy.status_code}, sell={response_sell.status_code}")
            return None

    except Exception as e:
        print(f"Ошибка при получении цен: {e}")
        return None


if __name__ == "__main__":
    # Пример использования
    # Замените на реальный market_id
    MARKET_ID = "your_market_id_here"

    # Мониторинг в течение 60 минут (или None для бесконечного мониторинга)
    log_market_prices(
        market_id=MARKET_ID,
        duration_minutes=60,
        log_file="polymarket_prices.json"
    )
