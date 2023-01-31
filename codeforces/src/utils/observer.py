from abc import abstractmethod, ABC


class ObserverI(ABC):
    @abstractmethod
    def update(self, value): pass


class ObserverSubjectI(ABC):
    @abstractmethod
    def attach(self, observer): pass

    @abstractmethod
    def detach(self, observer): pass

    @abstractmethod
    def notify(self, value): pass


class ObserverSubject(ObserverSubjectI):
    def __init__(self):
        self._observers = []

    def attach(self, observer: ObserverI):
        assert isinstance(observer, ObserverI)

        if observer not in self._observers:
            self._observers.append(observer)
            return True

    def detach(self, observer: ObserverI):
        assert isinstance(observer, ObserverI)

        if observer in self._observers:
            self._observers.remove(observer)
            return True

    def notify(self, value):
        for observer in self._observers:
            observer.update(value)

