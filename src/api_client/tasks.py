import json
import os
from multiprocessing import Process, Value, Lock
from .LoadTester import load_tests, abstract
from .LoadTester.proc_func import process_function
from .celery import app
from .models import TestCall, Result

import typing
import inspect
import requests

from datetime import datetime

from .serializers import TestCallSerializer


def filter_classes(o):
    return inspect.isclass(o) and 'LoadTesterBase' in map(lambda x: x.__name__, inspect.getmro(o))


@app.task
def run_test(test_call_str: str):
    test_call_dict = TestCallSerializer(test_call_str).instance
    test_call = TestCall.objects.get(pk = test_call_dict['id'])
    classes = inspect.getmembers(load_tests, filter_classes)
    print(classes)
    print(test_call)
    needed_class = list(filter(lambda x: x[0] == test_call.test.class_name, classes))
    if len(needed_class) != 1:
        raise TypeError('Cannot find described class: %s' % test_call.test.class_name)

    needed_class = needed_class[0]
    counter = Value('i', 0)
    lock = Lock()
    processes = []
    for i in range(test_call.num_users):
        proc = Process(target=process_function, args=(needed_class, test_call.max_calls, counter, lock, test_call_dict))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()

    result = requests.post("%s/rest-auth/login/" % os.getenv("BACKEND_URL"),
                           json={"username": os.getenv("BACKEND_USER"), "password": os.getenv("BACKEND_PASSWORD")})

    with open('prices%s.txt' % test_call.start_date.strftime("%m-%d-%Y %H-%M-%S"), 'w') as f:
        f.write(json.dumps(requests.get("%s/price_history/" % os.getenv("BACKEND_URL"), headers={"OBCIAZNIK": "DUPA", "Authorization": "Bearer %s" % result.json()['token']}).json()))

    with open('transactions%s.txt' % test_call.start_date.strftime("%m-%d-%Y %H-%M-%S"), 'w') as f:
        f.write(json.dumps(requests.get("%s/transaction/" % os.getenv("BACKEND_URL"), headers={"OBCIAZNIK": "DUPA", "Authorization": "Bearer %s" % result.json()['token']}).json()))

    test_call.is_finished = True
    test_call.end_date = datetime.now()
    test_call.save()

