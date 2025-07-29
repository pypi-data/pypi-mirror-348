# logger_manager.py
import logging
import sys
import types

class LoggerManager:
    _enable_logs = False
    _logger = logging.getLogger("app_logger")

    @classmethod
    def enable(cls):
        cls._enable_logs = True

    @classmethod
    def disable(cls):
        cls._enable_logs = False

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
                if LoggerManager._enable_logs:
                    super().emit(record)

        if not cls._logger.handlers:
            handler = ConditionalStreamHandler(sys.stdout)
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            cls._logger.setLevel(logging.DEBUG)
            cls._logger.addHandler(handler)

        def log_newline(self, num_lines=1):
            for _ in range(num_lines):
                if LoggerManager._enable_logs:
                    print('')

        cls._logger.newline = types.MethodType(log_newline, cls._logger)

# Executa o setup assim que o módulo é importado
LoggerManager.setup()

# Exporta o necessário
__all__ = ["LoggerManager"]
