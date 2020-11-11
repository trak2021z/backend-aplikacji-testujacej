from .celery import app
from .models import TestCall


@app.task
def run_test(test_call: TestCall):
    pass