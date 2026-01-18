"""
Сервис для непрерывного мониторинга нескольких рынков Polymarket
"""
import time
import json
import os
import sys
from datetime import datetime
from threading import Thread, Lock
from typing import Dict, List, Optional
import requests

# API endpoints
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"

# Глобальные переменные
config_lock = Lock()
current_config = None
last_config_mtime = 0
running_threads = {}


class MarketMonitor:
    """Класс для мониторинга отдельного рынка"""

    def __init__(self, slug: str, name: str, output_dir: str):
        self.slug = slug
        self.name = name
        self.output_dir = output_dir
        self.should_stop = False
        self.market_details = None
        self.token_id = None

    def initialize(self) -> bool:
        """Инициализация: получение деталей рынка и token_id"""
        try:
            self.market_details = get_market_details(self.slug)
            if not self.market_details:
                print(f"[{self.name}] Ошибка: не удалось получить детали рынка")
                return False

            # Получаем token_id
            clob_token_ids = self.market_details.get('clobTokenIds')
            if not clob_token_ids:
                print(f"[{self.name}] Ошибка: рынок не содержит токенов")
                return False

            token_ids = json.loads(clob_token_ids) if isinstance(clob_token_ids, str) else clob_token_ids
            self.token_id = token_ids[0] if isinstance(token_ids, list) and len(token_ids) > 0 else None

            if not self.token_id:
                print(f"[{self.name}] Ошибка: не удалось извлечь token_id")
                return False

            print(f"[{self.name}] Инициализация завершена")
            return True

        except Exception as e:
            print(f"[{self.name}] Ошибка инициализации: {e}")
            return False

    def get_log_filename(self) -> str:
        """Генерация имени файла для логирования"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_slug = self.slug.replace('/', '_').replace('\\', '_')
        return os.path.join(self.output_dir, f"{safe_slug}_{date_str}.json")

    def log_price(self, price_data: dict) -> bool:
        """Запись данных о цене в файл"""
        try:
            log_file = self.get_log_filename()

            # Создаем директорию если её нет
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

            # Читаем существующие данные или создаем новый файл
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
            else:
                logs = []

            # Добавляем новую запись
            timestamp = datetime.now().isoformat()
            log_entry = {
                "timestamp": timestamp,
                "market_slug": self.slug,
                "market_name": self.market_details.get('question', 'Unknown'),
                "token_id": self.token_id,
                "bid": price_data.get('bid'),
                "ask": price_data.get('ask'),
                "mid": price_data.get('mid')
            }

            logs.append(log_entry)

            # Записываем обратно в файл
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"[{self.name}] Ошибка записи в файл: {e}")
            return False

    def run(self, poll_interval: int):
        """Основной цикл мониторинга"""
        print(f"[{self.name}] Запуск мониторинга...")

        if not self.initialize():
            print(f"[{self.name}] Не удалось инициализировать монитор")
            return

        iteration = 0

        while not self.should_stop:
            try:
                # Получаем цены
                price_data = get_current_price(self.token_id)

                if price_data:
                    # Записываем в файл
                    if self.log_price(price_data):
                        iteration += 1
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"[{self.name}] [{timestamp}] Запись #{iteration}: "
                              f"Bid={price_data['bid']}, Ask={price_data['ask']}, Mid={price_data['mid']}")
                else:
                    print(f"[{self.name}] Не удалось получить цены")

            except Exception as e:
                print(f"[{self.name}] Ошибка в цикле мониторинга: {e}")

            # Ждем до следующей итерации
            for _ in range(poll_interval):
                if self.should_stop:
                    break
                time.sleep(1)

        print(f"[{self.name}] Мониторинг остановлен (записано {iteration} записей)")

    def stop(self):
        """Остановка мониторинга"""
        self.should_stop = True


def get_market_details(slug: str) -> Optional[dict]:
    """Получает детали рынка через Gamma API"""
    try:
        url = f"{GAMMA_API_BASE}/markets"
        params = {"slug": slug}
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0]
        return None

    except Exception as e:
        print(f"Ошибка при получении деталей рынка: {e}")
        return None


def get_current_price(token_id: str) -> Optional[dict]:
    """Получает текущие цены для токена через CLOB API"""
    try:
        url = f"{CLOB_API_BASE}/price"

        response_buy = requests.get(url, params={"token_id": token_id, "side": "buy"}, timeout=10)
        response_sell = requests.get(url, params={"token_id": token_id, "side": "sell"}, timeout=10)

        if response_buy.status_code == 200 and response_sell.status_code == 200:
            bid_data = response_buy.json()
            ask_data = response_sell.json()

            bid = float(bid_data.get('price', 0)) if bid_data.get('price') else None
            ask = float(ask_data.get('price', 0)) if ask_data.get('price') else None

            mid = None
            if bid is not None and ask is not None:
                mid = (bid + ask) / 2

            return {'bid': bid, 'ask': ask, 'mid': mid}

        return None

    except Exception as e:
        print(f"Ошибка при получении цен: {e}")
        return None


def load_config(config_file: str = "config.json") -> Optional[dict]:
    """Загрузка конфигурации из файла"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        return None


def get_config_mtime(config_file: str = "config.json") -> float:
    """Получение времени последней модификации файла конфигурации"""
    try:
        return os.path.getmtime(config_file)
    except:
        return 0


def start_monitor(market: dict, output_dir: str, poll_interval: int) -> Thread:
    """Запуск монитора для рынка в отдельном потоке"""
    monitor = MarketMonitor(
        slug=market['slug'],
        name=market.get('name', market['slug']),
        output_dir=output_dir
    )

    thread = Thread(target=monitor.run, args=(poll_interval,), daemon=True)
    thread.monitor = monitor  # Сохраняем ссылку на монитор
    thread.start()

    return thread


def config_reloader(config_file: str = "config.json"):
    """Поток для перезагрузки конфигурации"""
    global current_config, last_config_mtime, running_threads

    print(f"[Config Reloader] Запущен")

    while True:
        try:
            # Проверяем, изменился ли файл конфигурации
            current_mtime = get_config_mtime(config_file)

            if current_mtime > last_config_mtime:
                print(f"[Config Reloader] Обнаружены изменения в конфигурации")

                new_config = load_config(config_file)
                if new_config:
                    with config_lock:
                        # Определяем, какие рынки нужно остановить
                        old_slugs = {m['slug'] for m in current_config.get('markets', []) if m.get('enabled', True)}
                        new_slugs = {m['slug'] for m in new_config.get('markets', []) if m.get('enabled', True)}

                        # Останавливаем удаленные или отключенные рынки
                        for slug in old_slugs - new_slugs:
                            if slug in running_threads:
                                print(f"[Config Reloader] Остановка монитора: {slug}")
                                running_threads[slug].monitor.stop()
                                running_threads[slug].join(timeout=5)
                                del running_threads[slug]

                        # Запускаем новые рынки
                        for market in new_config.get('markets', []):
                            if market.get('enabled', True) and market['slug'] not in running_threads:
                                print(f"[Config Reloader] Запуск нового монитора: {market.get('name', market['slug'])}")
                                thread = start_monitor(
                                    market,
                                    new_config['settings']['output_directory'],
                                    new_config['settings']['poll_interval_seconds']
                                )
                                running_threads[market['slug']] = thread

                        current_config = new_config
                        last_config_mtime = current_mtime
                        print(f"[Config Reloader] Конфигурация обновлена")

        except Exception as e:
            print(f"[Config Reloader] Ошибка: {e}")

        # Ждем перед следующей проверкой
        if current_config:
            interval = current_config['settings'].get('config_reload_interval_seconds', 30)
        else:
            interval = 30
        time.sleep(interval)


def main():
    """Главная функция сервиса"""
    global current_config, last_config_mtime, running_threads

    # Настраиваем кодировку для Windows
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 60)
    print("Polymarket Price Monitor Service")
    print("=" * 60)
    print()

    # Загружаем начальную конфигурацию
    config_file = "config.json"
    current_config = load_config(config_file)

    if not current_config:
        print("Ошибка: не удалось загрузить конфигурацию")
        return

    last_config_mtime = get_config_mtime(config_file)

    # Создаем директорию для логов
    output_dir = current_config['settings']['output_directory']
    os.makedirs(output_dir, exist_ok=True)

    # Запускаем мониторы для всех активных рынков
    poll_interval = current_config['settings']['poll_interval_seconds']

    for market in current_config['markets']:
        if market.get('enabled', True):
            print(f"Запуск монитора: {market.get('name', market['slug'])}")
            thread = start_monitor(market, output_dir, poll_interval)
            running_threads[market['slug']] = thread

    print()
    print(f"Запущено мониторов: {len(running_threads)}")
    print(f"Директория для логов: {output_dir}")
    print(f"Интервал опроса: {poll_interval} секунд")
    print(f"Файл конфигурации: {config_file}")
    print()
    print("Для остановки нажмите Ctrl+C")
    print("=" * 60)
    print()

    # Запускаем поток для перезагрузки конфигурации
    reloader_thread = Thread(target=config_reloader, args=(config_file,), daemon=True)
    reloader_thread.start()

    try:
        # Основной цикл - просто ждем
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nОстановка сервиса...")

        # Останавливаем все мониторы
        with config_lock:
            for slug, thread in running_threads.items():
                print(f"Остановка монитора: {slug}")
                thread.monitor.stop()

            # Ждем завершения всех потоков
            for thread in running_threads.values():
                thread.join(timeout=5)

        print("Сервис остановлен")


if __name__ == "__main__":
    main()
