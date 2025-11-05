#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для получения курсов валют к рублю
- Фиатные валюты: API Центрального Банка РФ
- Криптовалюты: CoinGecko API
"""

import requests
from requests.exceptions import RequestException
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time


class CurrencyParser:
    """Класс для парсинга курсов валют"""
    
    # API ЦБ РФ для фиатных валют
    CBR_API_DAILY = "https://www.cbr.ru/scripts/XML_daily.asp"
    CBR_API_HISTORY = "https://www.cbr.ru/scripts/XML_dynamic.asp"
    
    # CoinGecko API для криптовалют
    COINGECKO_API = "https://api.coingecko.com/api/v3"
    
    # Основные фиатные валюты
    FIAT_CURRENCIES = {
        'USD': 'R01235',  # Доллар США
        'EUR': 'R01239',  # Евро
        'GBP': 'R01035',  # Фунт стерлингов
        'JPY': 'R01820',  # Японская йена
        'CNY': 'R01375',  # Китайский юань
        'CHF': 'R01775',  # Швейцарский франк
        'AUD': 'R01010',  # Австралийский доллар
        'CAD': 'R01350',  # Канадский доллар
        'NOK': 'R01535',  # Норвежская крона
        'SEK': 'R01770',  # Шведская крона
    }
    
    # Основные криптовалюты
    CRYPTO_CURRENCIES = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'BNB': 'binancecoin',
        'XRP': 'ripple',
        'ADA': 'cardano',
        'SOL': 'solana',
        'DOGE': 'dogecoin',
        'DOT': 'polkadot',
        'MATIC': 'matic-network',
        'LTC': 'litecoin',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_fiat_rate(self, currency_code: str, date: Optional[datetime] = None) -> Optional[float]:
        """
        Получает курс фиатной валюты к рублю
        
        Args:
            currency_code: Код валюты (USD, EUR, etc.)
            date: Дата для получения курса (если None - текущая дата)
        
        Returns:
            Курс валюты к рублю или None
        """
        if currency_code not in self.FIAT_CURRENCIES:
            return None
        
        if date is None:
            date = datetime.now()
        
        try:
            if date.date() == datetime.now().date():
                # Текущий курс
                url = f"{self.CBR_API_DAILY}?date_req={date.strftime('%d/%m/%Y')}"
            else:
                # Исторический курс
                valute_id = self.FIAT_CURRENCIES[currency_code]
                date_start = date.strftime('%d/%m/%Y')
                url = f"{self.CBR_API_HISTORY}?date_req1={date_start}&date_req2={date_start}&VAL_NM_RQ={valute_id}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            # Поиск валюты
            for valute in root.findall('Valute'):
                if valute.get('ID') == self.FIAT_CURRENCIES[currency_code]:
                    value_str = valute.find('Value').text.replace(',', '.')
                    return float(value_str)
            
            # Если не нашли в списке, пробуем по коду
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                if char_code == currency_code:
                    value_str = valute.find('Value').text.replace(',', '.')
                    return float(value_str)
            
            return None
        except Exception as e:
            print(f"Ошибка при получении курса {currency_code}: {e}")
            return None
    
    def get_fiat_rates_history(self, currency_code: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Получает историю курсов фиатной валюты
        
        Args:
            currency_code: Код валюты
            start_date: Начальная дата
            end_date: Конечная дата
        
        Returns:
            Список словарей с датами и курсами
        """
        if currency_code not in self.FIAT_CURRENCIES:
            return []
        
        valute_id = self.FIAT_CURRENCIES[currency_code]
        history = []
        
        try:
            date_start = start_date.strftime('%d/%m/%Y')
            date_end = end_date.strftime('%d/%m/%Y')
            url = f"{self.CBR_API_HISTORY}?date_req1={date_start}&date_req2={date_end}&VAL_NM_RQ={valute_id}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            for record in root.findall('Record'):
                date_str = record.get('Date')
                value_str = record.find('Value').text.replace(',', '.')
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                history.append({
                    'date': date_obj,
                    'rate': float(value_str),
                    'currency': currency_code
                })
            
            return sorted(history, key=lambda x: x['date'])
        except Exception as e:
            print(f"Ошибка при получении истории курса {currency_code}: {e}")
            return []
    
    def get_crypto_rate(self, currency_code: str) -> Optional[float]:
        """
        Получает текущий курс криптовалюты к рублю
        
        Args:
            currency_code: Код криптовалюты (BTC, ETH, etc.)
        
        Returns:
            Курс в рублях или None
        """
        if currency_code not in self.CRYPTO_CURRENCIES:
            return None
        
        try:
            coin_id = self.CRYPTO_CURRENCIES[currency_code]
            url = f"{self.COINGECKO_API}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'rub'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if coin_id in data and 'rub' in data[coin_id]:
                return data[coin_id]['rub']
            
            return None
        except Exception as e:
            print(f"Ошибка при получении курса криптовалюты {currency_code}: {e}")
            return None
    
    def get_crypto_rates_history(self, currency_code: str, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Получает историю курсов криптовалюты
        
        Args:
            currency_code: Код криптовалюты
            start_date: Начальная дата
            end_date: Конечная дата
        
        Returns:
            Список словарей с датами и курсами
        """
        if currency_code not in self.CRYPTO_CURRENCIES:
            return []
        
        coin_id = self.CRYPTO_CURRENCIES[currency_code]
        history = []
        
        try:
            # CoinGecko API использует timestamp в секундах
            start_timestamp = int(start_date.timestamp())
            end_timestamp = int(end_date.timestamp())
            
            url = f"{self.COINGECKO_API}/coins/{coin_id}/market_chart/range"
            params = {
                'vs_currency': 'rub',
                'from': start_timestamp,
                'to': end_timestamp
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'prices' in data and len(data['prices']) > 0:
                for price_data in data['prices']:
                    timestamp = price_data[0] / 1000  # Конвертируем из миллисекунд
                    date_obj = datetime.fromtimestamp(timestamp)
                    rate = price_data[1]
                    
                    # Фильтруем только даты в нужном диапазоне
                    if start_date <= date_obj <= end_date:
                        history.append({
                            'date': date_obj,
                            'rate': rate,
                            'currency': currency_code
                        })
            else:
                # Если данных нет, возможно API вернул ошибку
                if 'error' in data:
                    print(f"CoinGecko API ошибка: {data['error']}")
                else:
                    print(f"CoinGecko API вернул пустые данные для {currency_code}")
            
            return sorted(history, key=lambda x: x['date'])
        except RequestException as e:
            print(f"Ошибка сети при получении истории курса криптовалюты {currency_code}: {e}")
            return []
        except Exception as e:
            print(f"Ошибка при получении истории курса криптовалюты {currency_code}: {e}")
            return []
    
    def get_all_fiat_rates(self, date: Optional[datetime] = None) -> Dict[str, float]:
        """Получает все основные фиатные курсы"""
        rates = {}
        for currency in self.FIAT_CURRENCIES.keys():
            rate = self.get_fiat_rate(currency, date)
            if rate:
                rates[currency] = rate
            time.sleep(0.1)  # Небольшая задержка для избежания блокировки
        return rates
    
    def get_all_crypto_rates(self) -> Dict[str, float]:
        """Получает все основные криптовалютные курсы"""
        rates = {}
        try:
            coin_ids = ','.join(self.CRYPTO_CURRENCIES.values())
            url = f"{self.COINGECKO_API}/simple/price"
            params = {
                'ids': coin_ids,
                'vs_currencies': 'rub'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for currency_code, coin_id in self.CRYPTO_CURRENCIES.items():
                if coin_id in data and 'rub' in data[coin_id]:
                    rates[currency_code] = data[coin_id]['rub']
            
            return rates
        except Exception as e:
            print(f"Ошибка при получении криптовалютных курсов: {e}")
            return {}

