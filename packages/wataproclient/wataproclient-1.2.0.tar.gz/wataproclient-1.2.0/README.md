# WATA Pro API Client

Асинхронный модульный клиент для платежного API WATA Pro с расширенными возможностями отладки.

## 🚀 Установка

```bash
# Установка из локального проекта
pip install -e .

# Или установка через uv (рекомендуется)
uv add wataproclient
```

## ⚡ Быстрый старт

```python
import asyncio
import logging
from wataproclient import WataClient

async def main():
    # Инициализация клиента с базовым URL и JWT-токеном
    async with WataClient(
        base_url="https://api.wata.pro",  # Внимание: используйте именно этот формат URL!
        jwt_token="ваш_jwt_токен",
        log_level=logging.INFO  # Или DEBUG для подробного логирования
    ) as client:
        # Создание платежной ссылки
        payment_link = await client.links.create(
            amount=1188.00,
            currency="RUB",
            description="Оплата заказа №123",
            order_id="ORDER-123",
            success_redirect_url="https://example.com/success",
            fail_redirect_url="https://example.com/fail"
        )
        
        print(f"Создана платежная ссылка: {payment_link['url']}")
        
        # Получение информации о платежной ссылке по ID
        link_info = await client.links.get(payment_link["id"])
        print(f"Статус ссылки: {link_info['status']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Конфигурация base_url

**ВАЖНО!** Для корректной работы клиента используйте следующие форматы base_url:

```python
# ✅ ПРАВИЛЬНО
WataClient(base_url="https://api.wata.pro")
WataClient(base_url="https://api-sandbox.wata.pro")

# ❌ НЕПРАВИЛЬНО (дублирует путь)
WataClient(base_url="https://api.wata.pro/api/h2h/")
```

Модули автоматически добавляют необходимые пути к конечным точкам.

## 🐛 Отладка и логирование

Клиент включает подробную систему логирования для отладки проблем:

```python
import logging

# Включение подробного логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
)

# Создание клиента с debug логированием
client = WataClient(
    base_url="https://api.wata.pro",
    jwt_token="ваш_jwt_токен",
    log_level=logging.DEBUG  # Показывает все HTTP-запросы и ответы
)
```

### Что показывает debug логирование:
- 📤 **Исходящие запросы**: метод, URL, заголовки, тело запроса
- 📥 **Входящие ответы**: статус, заголовки, тело ответа
- 🔍 **Параметры методов**: все переданные в методы API параметры
- ⚙️ **Внутренние операции**: подготовка данных, результаты операций

## 📚 Возможности клиента

### Платежные ссылки (`client.links`)

```python
# Создание платежной ссылки
link = await client.links.create(
    amount=1000.00,
    currency="RUB",
    description="Описание платежа",
    order_id="ORDER-123",
    success_redirect_url="https://example.com/success",
    fail_redirect_url="https://example.com/fail",
    expiration_date_time="2024-06-01T12:00:00Z"
)

# Получение платежной ссылки по ID
link_info = await client.links.get("3fa85f64-5717-4562-b3fc-2c963f66afa6")

# Поиск платежных ссылок
links = await client.links.search(
    amount_from=1000.00,
    amount_to=2000.00,
    currencies=["RUB"],
    statuses=["Opened"],
    sorting="creationTime desc",
    max_result_count=20
)
```

### Транзакции (`client.transactions`)

```python
# Получение транзакции по ID
transaction = await client.transactions.get("3a16a4f0-27b0-09d1-16da-ba8d5c63eae3")

# Поиск транзакций
transactions = await client.transactions.search(
    creation_time_from="2024-05-01T00:00:00Z",
    creation_time_to="2024-05-31T23:59:59Z", 
    currencies=["RUB"],
    statuses=["Paid"],
    sorting="amount desc",
    max_result_count=50
)
```

### Верификация вебхуков (`client.webhooks`)

```python
# Проверка подписи вебхука
is_valid = await client.webhooks.verify_signature(
    raw_json_body=webhook_request_body,  # Сырые байты тела запроса вебхука
    signature_header=webhook_signature   # Значение заголовка X-Signature
)

if is_valid:
    # Обработка вебхука
    webhook_data = json.loads(webhook_request_body)
    print(f"Получен вебхук: {webhook_data}")
else:
    # Отклонение недействительного вебхука
    print("Недействительная подпись вебхука")
```

## 🚨 Обработка ошибок

Клиент предоставляет набор специализированных исключений для обработки различных ошибок API:

```python
from wataproclient import (
    ApiError,              # Базовое исключение
    ApiConnectionError,    # Ошибка соединения
    ApiTimeoutError,       # Тайм-аут запроса
    ApiAuthError,          # Ошибка аутентификации (401)
    ApiForbiddenError,     # Доступ запрещен (403)
    ApiResourceNotFoundError,  # Ресурс не найден (404)
    ApiValidationError,    # Ошибка валидации (400)
    ApiServerError,        # Ошибка сервера (500)
    ApiServiceUnavailableError,  # Сервис недоступен (503)
    ApiParsingError,       # Ошибка парсинга ответа
)

try:
    result = await client.links.create(amount=1000.00, currency="RUB")
except ApiAuthError:
    print("Ошибка аутентификации. Проверьте JWT-токен")
except ApiValidationError as e:
    print(f"Ошибка валидации: {e.message}")
except ApiConnectionError:
    print("Не удалось подключиться к API")
except ApiError as e:  # Перехватывает все ошибки API
    print(f"Ошибка API: {e.message}, код: {e.status_code}")
```

## ⚙️ Расширенная конфигурация

### Основные параметры клиента

```python
client = WataClient(
    base_url="https://api.wata.pro",
    jwt_token="ваш_jwt_токен",
    timeout=60,  # Таймаут запроса в секундах
    max_retries=5,  # Максимальное количество повторных попыток
    log_level=logging.DEBUG  # Уровень логирования
)
```

### Использование менеджера клиентов

```python
from wataproclient import WataClientManager

# Создание и регистрация клиента
WataClientManager.create(
    name="prod",
    base_url="https://api.wata.pro",
    jwt_token="prod_jwt_токен",
    timeout=60,
    max_retries=3
)

# Создание клиента для тестовой среды
WataClientManager.create(
    name="sandbox",
    base_url="https://api-sandbox.wata.pro",
    jwt_token="sandbox_jwt_токен",
    log_level=logging.DEBUG
)

# Получение и использование клиентов
prod_client = WataClientManager.get("prod")
sandbox_client = WataClientManager.get("sandbox")

# Параллельное использование клиентов
async with prod_client, sandbox_client:
    # Создание тестового платежа в песочнице
    test_link = await sandbox_client.links.create(
        amount=100.00, currency="RUB", description="Тест"
    )
    
    # Создание реального платежа в продакшне
    prod_link = await prod_client.links.create(
        amount=1000.00, currency="RUB", description="Продакшн"
    )

# Закрытие всех клиентов
await WataClientManager.close_all()
```

## 🧪 Тестирование и отладка

### Запуск тестового скрипта с отладкой

```bash
# Запуск теста с подробным логированием
cd path/to/wataClient
python debug_test.py
```

### Пример вывода debug логирования

```
2025-05-18 15:48:20 | DEBUG    | wataproclient.modules.links | *** ВЫЗОВ МЕТОДА LinksModule.create ***
2025-05-18 15:48:20 | DEBUG    | wataproclient.modules.links |   amount: 10.0
2025-05-18 15:48:20 | DEBUG    | wataproclient.modules.links |   currency: RUB
2025-05-18 15:48:20 | DEBUG    | wataproclient.http          | === ОТПРАВКА HTTP ЗАПРОСА ===
2025-05-18 15:48:20 | DEBUG    | wataproclient.http          | Метод: POST
2025-05-18 15:48:20 | DEBUG    | wataproclient.http          | Полный URL: https://api.wata.pro/api/h2h/links
2025-05-18 15:48:20 | DEBUG    | wataproclient.http          | Заголовки: {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJ...'}
2025-05-18 15:48:23 | DEBUG    | wataproclient.http          | === ПОЛУЧЕН HTTP ОТВЕТ ===
2025-05-18 15:48:23 | DEBUG    | wataproclient.http          | Статус ответа: 200
```

## 🔄 Повторные попытки и отказоустойчивость

Клиент автоматически повторяет запросы при временных сбоях:

- **Коды для повтора**: 502, 503, 504 (по умолчанию)
- **Стратегия задержки**: Экспоненциальная (backoff)
- **Максимальное количество попыток**: Настраивается через `max_retries`

## 📋 Требования

- **Python**: 3.7+
- **Зависимости**:
  - `aiohttp >= 3.7.4`
  - `cryptography`

## 📁 Файлы проекта

```
wataproclient/
├── debug_test.py          # Тестовый скрипт с подробным логированием
├── DEBUG_LOGGING.md       # Документация по отладке
├── example.py             # Примеры использования
└── src/wataproclient/
    ├── client.py          # Основной клиент
    ├── manager.py         # Менеджер клиентов
    ├── http.py            # HTTP-клиент с детальным логированием
    ├── exceptions.py      # Система исключений
    └── modules/           # API модули
        ├── base.py        # Базовый модуль с отладкой
        ├── links.py       # Платежные ссылки
        ├── transactions.py # Транзакции
        └── webhooks.py    # Верификация вебхуков
```

## 📖 Дополнительная документация

- [DEBUG_LOGGING.md](./DEBUG_LOGGING.md) - Подробное руководство по отладке
- [README-AI.md](./README-AI.md) - Техническая архитектура и внутреннее устройство

## 📜 Лицензия

MIT

---

## 💡 Полезные советы

1. **Проблемы с 401 ошибкой?** Проверьте правильность `base_url` и JWT-токена
2. **Нужна подробная отладка?** Включите `log_level=logging.DEBUG`
3. **Работаете с вебхуками?** Обязательно проверяйте подписи через `verify_signature()`
4. **Используете несколько сред?** Применяйте `WataClientManager` для управления клиентами
