import logging
import sys
import types

# Flag global (pode ser alterada depois dinamicamente)
enable_logs = False

# Custom handler que obedece a flag
class ConditionalStreamHandler(logging.StreamHandler):
    def emit(self, record):
        if enable_logs:
            super().emit(record)

# Função pra adicionar linha em branco
def log_newline(self, num_lines=1):
    for _ in range(num_lines):
        if enable_logs:
            print('')  # bypassa formatação de log

# Setup do logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = ConditionalStreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Cola o método newline
logger.newline = types.MethodType(log_newline, logger)

# Exporta o logger e a flag de controle
__all__ = ["logger", "enable_logs"]
