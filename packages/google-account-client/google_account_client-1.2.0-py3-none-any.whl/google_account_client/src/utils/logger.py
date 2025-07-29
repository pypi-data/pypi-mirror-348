# logger_manager.py
import logging
import sys
import types

class Logger:
    _enable_logs = False
    _logger = logging.getLogger("google_account_client")
    
    @classmethod
    def log(cls, msg: str, level: str = 'debug'):
        level = level.lower()

        if level == 'info':
            cls._logger.info(msg)
        elif level == 'warning':
            cls._logger.warning(msg)
        elif level == 'error':
            cls._logger.error(msg)
        else:
            cls._logger.debug(msg)
    
    @classmethod
    def newline(cls, num_lines: int = 1):
        cls._logger.newline(num_lines)

    @classmethod
    def set_logger_state(cls, state: bool):
        cls._enable_logs = state

    @classmethod
    def is_enabled(cls):
        return cls._enable_logs

    @classmethod
    def get_logger(cls):
        return cls._logger

    @classmethod
    def setup(cls):
        class ConditionalStreamHandler(logging.StreamHandler):
            def emit(self, record):
                if Logger._enable_logs:
                    super().emit(record)

        if not cls._logger.handlers:
            handler = ConditionalStreamHandler(sys.stdout)
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            cls._logger.setLevel(logging.DEBUG)
            cls._logger.addHandler(handler)

        def newline(self, num_lines=1):
            for _ in range(num_lines):
                if Logger._enable_logs:
                    print('')

        cls._logger.newline = types.MethodType(newline, cls._logger)

# Executa o setup assim que o módulo é importado
Logger.setup()

# Exporta o necessário
__all__ = ["LoggerManager"]