from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Test)
admin.site.register(TestCall)
admin.site.register(Result)
admin.site.register(Endpoint)
admin.site.register(TestEndpoint)