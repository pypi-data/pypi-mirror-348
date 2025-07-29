from ..utils.logger import Logger

class Config:
    ENABLE_LOGS = False

    @classmethod
    def update_configs(cls, configs: dict[str, any]):
        cls.ENABLE_LOGS = configs.get('enable_logs', cls.ENABLE_LOGS)
        
        Logger.set_logger_state(cls.ENABLE_LOGS)