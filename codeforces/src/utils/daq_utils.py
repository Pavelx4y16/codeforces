import dash_daq as daq

from codeforces.src.utils.observer import ObserverI


class GraduatedBar(daq.GraduatedBar, ObserverI):
    def update(self, value):
        self.value = value * 100

