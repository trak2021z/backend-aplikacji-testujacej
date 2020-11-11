import abc


class LoadTesterBase(abc.ABC):
    @abc.abstractmethod
    def set_up(self):
        pass

    @abc.abstractmethod
    def test_func(self):
        pass

    @abc.abstractmethod
    def tear_down(self):
        pass
