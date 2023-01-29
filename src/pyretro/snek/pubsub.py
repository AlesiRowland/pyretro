class KeyPressSubscriber:

    def __init__(self, current_state):
        self._current_state = current_state

    def notify(self):
        ...


class MoveDownSubscriber(KeyPressSubscriber):

    def notify(self):
