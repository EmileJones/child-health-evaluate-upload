import abc


class AbstractLogger(abc.ABC):
    @abc.abstractmethod
    def debug(self, message) -> None:
        pass

    @abc.abstractmethod
    def info(self, message) -> None:
        pass

    @abc.abstractmethod
    def warn(self, message) -> None:
        pass

    @abc.abstractmethod
    def error(self, message) -> None:
        pass
