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

from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^activetest/$', v.ActiveTestCallView.as_view(), name='activeTestCall_view'),
    url(r'^test/$', v.TestView.as_view(), name='tests_view'),
    url(r'^test/(?P<pk>\d+)/$', v.TestView.as_view(), name='test_view'),
    url(r'^test/result/$', v.ResultView.as_view(), name='results_view'),
    url(r'^test/(?P<pk>\d+)/result/$', v.ResultView.as_view(), name='result_view'),
    url(r'^test/(?P<pk>\d+)/$', v.TestView.as_view(), name='test_view'),
    url(r'^test/call/(?P<pk>\d+)/$', v.TestCallView.as_view(), name='test_view'),
    url(r'^test/call/$', v.TestCallView.as_view(), name='test_view'),
    url(r'^test/call/(?P<pk>\d+)/details/$', v.TestCallDetailsView.as_view(), name='test_view'),
    url(r'^test/call/(?P<pk>\d+)/json/$', v.TestCallJsonView.as_view(), name='test_call_json_view'),
    url(r'^test/call/(?P<pk>\d+)/csv/$', v.TestCallCSVView.as_view(), name='test_call_csv_view'),
    url(r'^test/call/date/(?P<test_date>[\w\-]+)/$', v.TestCallByDateView.as_view(), name='test_view'),
    url(r'^test/call/date/$', v.TestCallByDateView.as_view(), name='test_view'),
]
