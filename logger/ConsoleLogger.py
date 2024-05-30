from logger.AbstractLogger import AbstractLogger


class ConsoleLogger(AbstractLogger):
    def debug(self, message) -> None:
        print("DEBUG: " + message)
        pass

    def error(self, message) -> None:
        print("ERROR: " + message)
        pass

    def info(self, message) -> None:
        print("INFO: " + message)
        pass

    def warn(self, message) -> None:
        print("WARN: " + message)
        pass
