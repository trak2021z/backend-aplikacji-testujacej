from multiprocessing import Process, Value, Lock
from .LoadTester import load_tests, abstract
from .celery import app
from .models import TestCall

import typing
import inspect
import requests

from datetime import datetime


class CounterExceeded(Exception):
    pass


class CountedRequestsWrapper(object):
    def __init__(self, counter: Value, lock: Lock, max_requests: int, test_call: TestCall):
        self.counter = counter
        self.lock = lock
        self.max_requests = max_requests

    def increment_counter(self):
        with self.lock:
            if self.counter.value >= self.max_requests:
                raise CounterExceeded()
            self.counter.value += 1

    def get(self, url, params=None, **kwargs):
        self.increment_counter()
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.get(url, params, **kwargs)
        return result

    def post(self, url, data=None, json=None, **kwargs):
        self.increment_counter()
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.post(url, data, json, **kwargs)
        return result

    def put(self, url, data=None, json=None, **kwargs):
        self.increment_counter()
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.put(url, data, json, **kwargs)
        return result

    def patch(self, url, data=None, json=None, **kwargs):
        self.increment_counter()
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.patch(url, data, json, **kwargs)
        return result

    def delete(self, url, **kwargs):
        self.increment_counter()
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.delete(url, **kwargs)
        return result


def filter_classes(o):
    return inspect.isclass(o) and 'LoadTesterBase' in map(lambda x: x.__name__, inspect.getmro(o))


def process_function(cls: typing.Type[abstract.LoadTesterBase], max_requests: int, counter: Value, lock: Lock, test_call):
    counted_requests = CountedRequestsWrapper(counter, lock, max_requests, test_call)
    obj = cls(counted_requests)
    obj.set_up()
    try:
        obj.test_func()
    except CounterExceeded:
        pass
    obj.tear_down()


@app.task
def run_test(test_call: TestCall):
    classes = inspect.getmembers(load_tests, filter_classes)
    needed_class = list(filter(lambda x: x.__name__ == test_call.test.class_name, classes))
    if len(needed_class) != 1:
        raise TypeError('Cannot find described class: %s' % test_call.test.class_name)

    needed_class = needed_class[0]
    counter = Value('i', 0)
    lock = Lock()
    processes = [Process(target=process_function, args=(needed_class, test_call.max_calls, counter, lock, test_call)) for i in range(test_call.num_users)]
    map(lambda x: x.start(), processes)
    for proc in processes:
        proc.join()

    test_call.is_finished = True
    test_call.end_date = datetime.now()
    test_call.save()

