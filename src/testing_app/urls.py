"""testing_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
import api_client.views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^test/$', v.TestView.as_view(), name='tests_view'),
    url(r'^test/(?P<pk>\d+)/$', v.TestView.as_view(), name='test_view'),
    url(r'^test/result/$', v.ResultView.as_view(), name='results_view'),
    url(r'^test/(?P<pk>\d+)/result/$', v.ResultView.as_view(), name='result_view'),
    url(r'^test/(?P<pk>\d+)/$', v.TestView.as_view(), name='test_view'),
    url(r'^test/result/(?P<pk>\d+)/$', v.TestResultView.as_view(), name='test_view'),
    url(r'^test/result/date/(?P<test_date>[\w\-]+)/$', v.TestResultByDateView.as_view(), name='test_view'),
    url(r'^test/result/date/$', v.TestResultByDateView.as_view(), name='test_view'),
]
