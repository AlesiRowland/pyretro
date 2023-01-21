import abc


class ControllerCommand(abc.ABC):
    def __init__(self, controller: "SnakeGameController") -> None:  # noqa
        self._controller = controller

    @abc.abstractmethod
    def execute(self) -> None:
        ...
