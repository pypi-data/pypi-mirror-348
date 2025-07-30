"""
Основной класс клиента WATA API.
"""
import logging
from typing import Optional

from .http import AsyncHttpClient
from .modules import LinksModule, TransactionsModule, WebhooksModule

class WataClient:
    """Клиент для платежного API WATA."""

    def __init__(
        self,
        base_url: str,
        jwt_token: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        log_level: int = logging.INFO,
    ):
        """
        Инициализация клиента WATA API.

        Аргументы:
            base_url: Базовый URL API (продакшн или песочница)
            jwt_token: JWT-токен для аутентификации
            timeout: Таймаут запроса в секундах
            max_retries: Максимальное количество попыток повтора
            log_level: Уровень логирования
        """
        # Сохраняем уровень логирования для передачи в компоненты
        self.log_level = log_level
        
        # Настройка логирования - НЕ добавляем обработчики, если они уже есть
        self.logger = logging.getLogger("wataproclient")
        
        # Устанавливаем уровень только для нашего логгера
        self.logger.setLevel(log_level)
        
        # Принудительно настраиваем уровни для всех дочерних логгеров
        self._configure_child_loggers(log_level)
        
        # Добавляем обработчик только если его нет и корневой логгер не настроен
        if not self.logger.handlers and not logging.getLogger().handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            handler.setLevel(log_level)
            self.logger.addHandler(handler)

        self.logger.info(f"Инициализация клиента WATA с базовым URL: {base_url}")
        
        # Инициализация HTTP-клиента
        self.http = AsyncHttpClient(
            base_url=base_url,
            jwt_token=jwt_token,
            timeout=timeout,
            max_retries=max_retries,
        )
        
        # Инициализация модулей API
        self.links = LinksModule(self.http)
        self.transactions = TransactionsModule(self.http)
        self.webhooks = WebhooksModule(self.http)
        
    def _configure_child_loggers(self, log_level: int):
        """Настройка уровней логирования для всех дочерних логгеров."""
        child_logger_names = [
            "wataproclient.http",
            "wataproclient.modules.base",
            "wataproclient.modules.links", 
            "wataproclient.modules.transactions",
            "wataproclient.modules.webhooks"
        ]
        
        for logger_name in child_logger_names:
            child_logger = logging.getLogger(logger_name)
            child_logger.setLevel(log_level)
            # Разрешаем передачу сообщений родительскому логгеру
            child_logger.propagate = True

    async def close(self) -> None:
        """Закрыть HTTP-сессию."""
        await self.http.close()

    async def __aenter__(self):
        """Вход в контекстный менеджер."""
        self.logger.debug("Вход в контекстный менеджер")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера."""
        self.logger.debug("Выход из контекстного менеджера")
        await self.close()
