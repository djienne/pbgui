class Logging:

    LEVEL = {
        0: "warnings",
        1: "info",
        2: "debug",
        3: "trace"}

    def __init__(self):
        self._level = 1
        self._logging = {
            "level": self._level
        }
    
    def __repr__(self):
        return str(self._logging)

    @property
    def logging(self): return self._logging
    @logging.setter
    def logging(self, new_logging):
        if "level" in new_logging:
            self.level = new_logging["level"]
    
    @property
    def level(self): return self._level
    @level.setter
    def level(self, new_level):
        self._level = new_level
        self._logging["level"] = self._level
