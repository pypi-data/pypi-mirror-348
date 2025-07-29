from ..auxiliar import LoggerManager

class GoogleInterface():
    def __init__(self):
        raise TypeError(f'Class {self.__class__.__name__} cannot be instantiated directly')
    
    def log(self, msg: str, level: str = 'debug', show_name: bool = False):
        if show_name:
            msg = f'({self.name}) {msg}'

        logger = LoggerManager.get_logger()
        level = level.lower()

        if level == 'info':
            logger.info(msg)
        elif level == 'warning':
            logger.warning(msg)
        elif level == 'error':
            logger.error(msg)
        else:
            logger.debug(msg)

    @staticmethod
    def log_newline(num_lines: int = 1):
        LoggerManager.get_logger().newline(num_lines)