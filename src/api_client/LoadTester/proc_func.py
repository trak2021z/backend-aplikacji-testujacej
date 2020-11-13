import json as js
import typing

from multiprocessing import Process, Value, Lock
import requests

from api_client.LoadTester import abstract


class CounterExceeded(Exception):
    pass


class CountedRequestsWrapper(object):
    def __init__(self, counter: Value, lock: Lock, max_requests: int, test_call):
        self.counter = counter
        self.lock = lock
        self.max_requests = max_requests
        self.test_call = test_call

    def increment_counter(self):
        with self.lock:
            if self.counter.value >= self.max_requests:
                raise CounterExceeded()
            self.counter.value += 1

    def get_stats_data(self, result):
        data = {}
        if 'num_sql_queries' in result.headers:
            data['num_sql_queries'] = int(result.headers['num_sql_queries'])
        if 'time_spent_on_sql_queries' in result.headers:
            data['time_spent_on_sql_queries'] = float(result.headers['time_spent_on_sql_queries'])
        if 'time_taken' in result.headers:
            data['time_taken'] = float(result.headers['time_taken'])
        if 'cpu_usage_current' in result.headers:
            data['cpu_usage_current'] = js.loads(result.headers['cpu_usage_current'])
        if 'cpu_usage_aggregated' in result.headers:
            data['cpu_usage_aggregated'] = js.loads(result.headers['cpu_usage_aggregated'])
        if 'cpu_time_spent_user' in result.headers:
            data['cpu_time_spent_user'] = float(result.headers['cpu_time_spent_user'])
        if 'cpu_time_spent_system' in result.headers:
            data['cpu_time_spent_system'] = float(result.headers['cpu_time_spent_system'])
        if 'cpu_time_spent_idle' in result.headers:
            data['cpu_time_spent_idle'] = float(result.headers['cpu_time_spent_idle'])
        if 'memory_usage' in result.headers:
            data['memory_usage'] = float(result.headers['memory_usage'])
        if 'container_id' in result.headers:
            data['container_id'] = result.headers['container_id']
        return data

    def get(self, url, params=None, **kwargs):
        from api_client.models import Result
        self.increment_counter()
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.get(url, params, **kwargs)
        Result.objects.create(test_call=self.test_call, results=js.dumps(self.get_stats_data(result)))
        return result

    def post(self, url, data=None, json=None, **kwargs):
        from api_client.models import Result
        self.increment_counter()
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.post(url, data, json, **kwargs)
        Result.objects.create(test_call=self.test_call, results=js.dumps(self.get_stats_data(result)))
        return result

    def put(self, url, data=None, json=None, **kwargs):
        from api_client.models import Result
        self.increment_counter()
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.put(url, data, json, **kwargs)
        Result.objects.create(test_call=self.test_call, results=js.dumps(self.get_stats_data(result)))
        return result

    def patch(self, url, data=None, json=None, **kwargs):
        from api_client.models import Result
        self.increment_counter()
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.patch(url, data, json, **kwargs)
        Result.objects.create(test_call=self.test_call, results=js.dumps(self.get_stats_data(result)))
        return result

    def delete(self, url, **kwargs):
        from api_client.models import Result
        self.increment_counter()
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['OBCIAZNIK'] = "KANAPKA"
        result = requests.delete(url, **kwargs)
        Result.objects.create(test_call=self.test_call, results=js.dumps(self.get_stats_data(result)))
        return result


def process_function(cls: typing.Type[abstract.LoadTesterBase], max_requests: int, counter: Value, lock: Lock, test_call_dict):
    import django
    django.setup()
    from api_client.models import TestCall
    test_call = TestCall.objects.get(pk=test_call_dict['id'])
    counted_requests = CountedRequestsWrapper(counter, lock, max_requests, test_call)
    obj = cls[1](counted_requests)
    obj.set_up()
    try:
        obj.test_func()
    except CounterExceeded:
        pass
    obj.tear_down()
