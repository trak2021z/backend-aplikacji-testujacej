from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=150, default="")

class TestCall(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='calls')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    num_users = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    max_calls = models.PositiveBigIntegerField(default=1)

class Result(models.Model):
    test_call = models.ForeignKey('TestCall', on_delete=models.CASCADE, related_name='results')
    results = models.TextField()

class Endpoint(models.Model):
    url = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=50, default="")
    request = models.TextField()

class TestEndpoint(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='test_endpoints')
    endpoint = models.ForeignKey('Endpoint', on_delete=models.CASCADE, related_name='test_endpoints')
    order = models.PositiveIntegerField(default=0)