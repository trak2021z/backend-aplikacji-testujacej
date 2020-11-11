import abc
import requests


class LoadTesterBase(abc.ABC):
    def __init__(self, counted_requests):
        self.counted_requests = counted_requests

    @abc.abstractmethod
    def set_up(self):
        pass

    @abc.abstractmethod
    def test_func(self):
        pass

    @abc.abstractmethod
    def tear_down(self):
        pass
