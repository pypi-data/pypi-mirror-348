from ..models.auxiliar.logger import logger

class Config:
    PORT = 8080
    ENABLE_LOGS = False

    @classmethod
    def update_configs(cls, configs: dict[str, any]):
        cls.PORT = configs.get('port', cls.PORT)
        cls.ENABLE_LOGS = configs.get('enable_logs', cls.ENABLE_LOGS)
        
        logger.enable_logs = cls.ENABLE_LOGS