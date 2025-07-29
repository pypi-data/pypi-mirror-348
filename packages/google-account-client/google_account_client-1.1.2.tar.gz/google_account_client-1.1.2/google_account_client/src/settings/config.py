from ..models.auxiliar import LoggerManager
LoggerManager.enable()

class Config:
    PORT = 8080
    ENABLE_LOGS = False

    @classmethod
    def update_configs(cls, configs: dict[str, any]):
        cls.PORT = configs.get('port', cls.PORT)
        cls.ENABLE_LOGS = configs.get('enable_logs', cls.ENABLE_LOGS)
        
        if cls.ENABLE_LOGS:
            LoggerManager.enable()
        else:
            LoggerManager.disable()