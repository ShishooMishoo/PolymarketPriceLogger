"""
Сервис для непрерывного мониторинга нескольких рынков Polymarket
"""
import time
import json
import sys
from datetime import datetime
from threading import Thread, Lock
from typing import Dict, Optional, Any, Tuple
from pathlib import Path

from api_client import get_market_details, get_current_price, extract_token_id

# Глобальная блокировка для конфигурации
config_lock = Lock()

class MarketMonitor:
    """Класс для мониторинга отдельного рынка"""

    def __init__(self, slug: str, name: str, output_dir: str):
        self.slug = slug
        self.name = name
        self.output_dir = Path(output_dir)
        self.should_stop = False
        self.market_details: Optional[Dict[str, Any]] = None
        self.token_id: Optional[str] = None

    def initialize(self) -> bool:
        """Инициализация: получение деталей рынка и token_id"""
        try:
            self.market_details = get_market_details(self.slug)
            if not self.market_details:
                print(f"[{self.name}] Ошибка: не удалось получить детали рынка")
                return False

            self.token_id = extract_token_id(self.market_details)

            if not self.token_id:
                print(f"[{self.name}] Ошибка: не удалось извлечь token_id")
                return False

            print(f"[{self.name}] Инициализация завершена")
            return True

        except Exception as e:
            print(f"[{self.name}] Ошибка инициализации: {e}")
            return False

    def get_log_filename(self) -> Path:
        """Генерация имени файла для логирования"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_slug = self.slug.replace('/', '_').replace('\\', '_')
        return self.output_dir / f"{safe_slug}_{date_str}.json"

    def log_price(self, price_data: Dict[str, Optional[float]]) -> bool:
        """Запись данных о цене в файл"""
        try:
            log_file = self.get_log_filename()

            # Создаем директорию если её нет
            log_file.parent.mkdir(parents=True, exist_ok=True)

            # Читаем существующие данные или создаем новый файл
            logs = []
            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content:
                            logs = json.loads(content)
                except json.JSONDecodeError:
                    logs = []
                except Exception as e:
                    print(f"[{self.name}] Ошибка чтения лога: {e}")
            
            market_question = 'Unknown'
            if self.market_details:
                 market_question = self.market_details.get('question', 'Unknown')

            # Добавляем новую запись
            timestamp = datetime.now().isoformat()
            log_entry = {
                "timestamp": timestamp,
                "market_slug": self.slug,
                "market_name": market_question,
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
                if self.token_id:
                    # Получаем цены
                    price_data = get_current_price(self.token_id)

                    if price_data:
                        # Записываем в файл
                        if self.log_price(price_data):
                            iteration += 1
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"[{self.name}] [{timestamp}] Запись #{iteration}: "
                                  f"Bid={price_data.get('bid')}, Ask={price_data.get('ask')}, Mid={price_data.get('mid')}")
                    else:
                        print(f"[{self.name}] Не удалось получить цены")
                else:
                    print(f"[{self.name}] Token ID потерян")

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


class ServiceManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.current_config: Optional[Dict[str, Any]] = None
        self.last_config_mtime: float = 0
        self.running_monitors: Dict[str, Tuple[Thread, MarketMonitor]] = {}
        self.should_stop = False

    def load_config(self) -> Optional[Dict[str, Any]]:
        """Загрузка конфигурации из файла"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            return None

    def get_config_mtime(self) -> float:
        """Получение времени последней модификации файла конфигурации"""
        try:
            return Path(self.config_file).stat().st_mtime
        except OSError:
            return 0.0

    def start_monitor(self, market: Dict[str, Any], output_dir: str, poll_interval: int) -> Tuple[Thread, MarketMonitor]:
        """Запуск монитора для рынка в отдельном потоке"""
        monitor = MarketMonitor(
            slug=market['slug'],
            name=market.get('name', market['slug']),
            output_dir=output_dir
        )

        thread = Thread(target=monitor.run, args=(poll_interval,), daemon=True)
        thread.start()

        return thread, monitor

    def update_monitors(self):
        """Обновление запущенных мониторов на основе конфигурации"""
        with config_lock:
            if not self.current_config:
                return

            new_config = self.current_config
            
            # Определяем, какие рынки нужно остановить
            # A market is kept if it exists in new config AND is enabled
            new_markets_map = {m['slug']: m for m in new_config.get('markets', []) if m.get('enabled', True)}
            
            # Identify monitors to stop (running but not in new valid markets)
            slugs_to_stop = []
            for slug in self.running_monitors:
                if slug not in new_markets_map:
                    slugs_to_stop.append(slug)
            
            # Stop removed/disabled markets
            for slug in slugs_to_stop:
                print(f"[Service] Остановка монитора: {slug}")
                thread, monitor = self.running_monitors[slug]
                monitor.stop()
                thread.join(timeout=5)
                del self.running_monitors[slug]

            # Start new markets
            settings = new_config.get('settings', {})
            output_dir = settings.get('output_directory', 'logs')
            poll_interval = settings.get('poll_interval_seconds', 60)

            for slug, market in new_markets_map.items():
                if slug not in self.running_monitors:
                    print(f"[Service] Запуск нового монитора: {market.get('name', slug)}")
                    thread, monitor = self.start_monitor(market, output_dir, poll_interval)
                    self.running_monitors[slug] = (thread, monitor)

    def config_reloader_loop(self):
        """Цикл перезагрузки конфигурации"""
        print(f"[Config Reloader] Запущен")

        while not self.should_stop:
            try:
                # Проверяем, изменился ли файл конфигурации
                current_mtime = self.get_config_mtime()

                if current_mtime > self.last_config_mtime:
                    print(f"[Config Reloader] Обнаружены изменения в конфигурации")

                    new_config = self.load_config()
                    if new_config:
                        self.current_config = new_config
                        self.last_config_mtime = current_mtime
                        self.update_monitors()
                        print(f"[Config Reloader] Конфигурация обновлена")

            except Exception as e:
                print(f"[Config Reloader] Ошибка: {e}")

            # Ждем перед следующей проверкой
            interval = 30
            if self.current_config:
                interval = self.current_config.get('settings', {}).get('config_reload_interval_seconds', 30)
            
            time.sleep(interval)

    def run(self):
        """Главный цикл сервиса"""
        # Настраиваем кодировку для Windows
        if sys.platform == 'win32':
             if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8') # type: ignore

        print("=" * 60)
        print("Polymarket Price Monitor Service")
        print("=" * 60)
        print()

        # Загружаем начальную конфигурацию
        self.current_config = self.load_config()

        if not self.current_config:
            print("Ошибка: не удалось загрузить конфигурацию")
            return

        self.last_config_mtime = self.get_config_mtime()

        # Создаем директорию для логов
        settings = self.current_config.get('settings', {})
        output_dir = settings.get('output_directory', 'logs')
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Запускаем начальные мониторы
        self.update_monitors()

        print()
        print(f"Запущено мониторов: {len(self.running_monitors)}")
        print(f"Директория для логов: {output_dir}")
        print(f"Файл конфигурации: {self.config_file}")
        print()
        print("Для остановки нажмите Ctrl+C")
        print("=" * 60)
        print()

        # Запускаем поток для перезагрузки конфигурации
        reloader_thread = Thread(target=self.config_reloader_loop, daemon=True)
        reloader_thread.start()

        try:
            # Основной цикл - просто ждем
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\nОстановка сервиса...")
            self.should_stop = True

            # Останавливаем все мониторы
            with config_lock:
                for slug, (thread, monitor) in self.running_monitors.items():
                    print(f"Остановка монитора: {slug}")
                    monitor.stop()

                # Ждем завершения всех потоков
                for slug, (thread, monitor) in self.running_monitors.items():
                    thread.join(timeout=5)
            
            print("Сервис остановлен")

if __name__ == "__main__":
    manager = ServiceManager()
    manager.run()
