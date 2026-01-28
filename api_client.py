import requests
from typing import Optional, Dict, Any, List, Union
import json

# API endpoints
GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"

def get_market_details(market_id: str) -> Optional[Dict[str, Any]]:
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

        # Use a timeout for network operations
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # API возвращает массив, берем первый элемент
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            print(f"Ошибка: рынок '{market_id}' не найден")
            return None
        else:
            print(f"Ошибка API (get_market_details): {response.status_code}")
            return None

    except Exception as e:
        print(f"Ошибка при получении деталей рынка: {e}")
        return None

def get_current_price(token_id: str) -> Optional[Dict[str, Optional[float]]]:
    """
    Получает текущие цены для токена через CLOB API.

    Args:
        token_id: ID токена

    Returns:
        dict: Данные цен (bid, ask, mid) или None при ошибке
    """
    try:
        url = f"{CLOB_API_BASE}/price"
        
        # We can use a session here for efficiency if we were making many calls rapidly,
        # but for this frequency, simple requests are fine.
        
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

def extract_token_id(market_details: Dict[str, Any]) -> Optional[str]:
    """
    Extracts the YES token ID from market details.
    """
    clob_token_ids = market_details.get('clobTokenIds')
    if not clob_token_ids:
        print("Ошибка: рынок не содержит токенов")
        return None

    # clobTokenIds - это JSON строка, парсим её
    token_ids = json.loads(clob_token_ids) if isinstance(clob_token_ids, str) else clob_token_ids

    # Берем первый токен (YES)
    token_id = token_ids[0] if isinstance(token_ids, list) and len(token_ids) > 0 else None
    
    return token_id
