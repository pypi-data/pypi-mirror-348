"""
Утилиты для настройки логирования клиента WATA в приложениях.
"""
import logging
import sys
from typing import Optional


class WataLoggingConfig:
    """Конфигуратор логирования для клиента WATA."""
    
    @staticmethod
    def setup_debug_logging(
        format_string: Optional[str] = None,
        stream = None,
        force_configure: bool = False
    ):
        """
        Настройка подробного debug логирования для клиента WATA.
        
        Используйте эту функцию в своем приложении для включения
        подробного логирования всех операций клиента WATA.
        
        Аргументы:
            format_string: Формат сообщений логирования
            stream: Поток для вывода (по умолчанию sys.stdout)
            force_configure: Принудительная настройка даже если логгер уже настроен
        
        Пример:
            from wataproclient.logging_config import WataLoggingConfig
            
            # Включить подробное логирование перед созданием клиента
            WataLoggingConfig.setup_debug_logging()
            
            # Создать клиент
            client = WataClient(..., log_level=logging.DEBUG)
        """
        if stream is None:
            stream = sys.stdout
            
        if format_string is None:
            format_string = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        
        # Настраиваем корневой логгер wataproclient
        wata_logger = logging.getLogger("wataproclient")
        
        # Проверяем, нужно ли настраивать
        if not force_configure and wata_logger.handlers:
            print("Логирование WATA уже настроено. Используйте force_configure=True для принудительной настройки.")
            return
        
        # Устанавливаем уровень DEBUG
        wata_logger.setLevel(logging.DEBUG)
        
        # Создаем обработчик
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.DEBUG)
        
        # Создаем форматтер
        formatter = logging.Formatter(
            format_string,
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        
        # Добавляем обработчик
        wata_logger.addHandler(handler)
        
        # Настраиваем все дочерние логгеры
        child_loggers = [
            "wataproclient.http",
            "wataproclient.modules.base",
            "wataproclient.modules.links",
            "wataproclient.modules.transactions", 
            "wataproclient.modules.webhooks"
        ]
        
        for logger_name in child_loggers:
            child_logger = logging.getLogger(logger_name)
            child_logger.setLevel(logging.DEBUG)
            child_logger.propagate = True
        
        print("✅ Debug логирование WATA настроено успешно")
    
    @staticmethod
    def setup_production_logging(
        level: int = logging.INFO,
        format_string: Optional[str] = None,
        stream = None
    ):
        """
        Настройка продакшн логирования для клиента WATA.
        
        Аргументы:
            level: Уровень логирования (по умолчанию INFO)
            format_string: Формат сообщений логирования
            stream: Поток для вывода (по умолчанию sys.stdout)
        """
        if stream is None:
            stream = sys.stdout
            
        if format_string is None:
            format_string = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        
        # Настраиваем корневой логгер wataproclient
        wata_logger = logging.getLogger("wataproclient")
        wata_logger.setLevel(level)
        
        if not wata_logger.handlers:
            handler = logging.StreamHandler(stream)
            handler.setLevel(level)
            
            formatter = logging.Formatter(
                format_string,
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            wata_logger.addHandler(handler)
        
        print(f"✅ Production логирование WATA настроено на уровне {logging.getLevelName(level)}")
    
    @staticmethod
    def disable_wata_logging():
        """Отключить все логирование клиента WATA."""
        wata_logger = logging.getLogger("wataproclient")
        wata_logger.disabled = True
        print("❌ Логирование WATA отключено")
        
    @staticmethod
    def get_wata_logger_status():
        """Получить информацию о состоянии логгеров WATA."""
        root_logger = logging.getLogger("wataproclient")
        
        print("🔍 Статус логгеров WATA:")
        print(f"  Корневой логгер 'wataproclient':")
        print(f"    Уровень: {logging.getLevelName(root_logger.level)}")
        print(f"    Отключен: {root_logger.disabled}")
        print(f"    Обработчиков: {len(root_logger.handlers)}")
        print(f"    Propagate: {root_logger.propagate}")
        
        child_loggers = [
            "wataproclient.http",
            "wataproclient.modules.base", 
            "wataproclient.modules.links",
            "wataproclient.modules.transactions",
            "wataproclient.modules.webhooks"
        ]
        
        for logger_name in child_loggers:
            logger = logging.getLogger(logger_name)
            print(f"  {logger_name}:")
            print(f"    Уровень: {logging.getLevelName(logger.level)}")
            print(f"    Обработчиков: {len(logger.handlers)}")
            print(f"    Propagate: {logger.propagate}")


def enable_wata_debug_logging(format_string: Optional[str] = None):
    """
    Простая функция для быстрого включения debug логирования.
    
    Пример использования:
        from wataproclient.logging_config import enable_wata_debug_logging
        
        # Включаем debug логирование
        enable_wata_debug_logging()
        
        # Создаем клиент
        client = WataClient(..., log_level=logging.DEBUG)
    """
    WataLoggingConfig.setup_debug_logging(format_string=format_string)
