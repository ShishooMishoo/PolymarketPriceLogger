import time
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from api_client import get_market_details, get_current_price, extract_token_id

def log_market_prices(market_id: str, duration_minutes: Optional[int] = None, log_file: str = "price_log.json"):
    """
    Мониторит указанный рынок Polymarket и записывает лучшие bid/ask цены каждую минуту.

    Args:
        market_id: ID рынка Polymarket для мониторинга
        duration_minutes: Длительность мониторинга в минутах (None = бесконечно)
        log_file: Имя файла для записи логов
    """
    # Настраиваем кодировку для Windows консоли
    if sys.platform == 'win32':
        # sys.stdout.reconfigure is available in Python 3.7+
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')

    print(f"Начинаю мониторинг рынка {market_id}")
    print(f"Данные будут записываться в {log_file}")

    log_path = Path(log_file)

    # Создаем файл, если его нет
    if not log_path.exists():
        with open(log_path, 'w', encoding='utf-8') as f:
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

                # Получаем token_id
                token_id = extract_token_id(market_details)
                
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
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    logs = []

                # Добавляем новую запись
                logs.append(log_entry)

                # Записываем обратно в файл
                with open(log_path, 'w', encoding='utf-8') as f:
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
