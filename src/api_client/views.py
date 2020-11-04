from django.shortcuts import render

# Create your views here.
from drf_yasg2.utils import swagger_auto_schema, is_list_view
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from .serializers import *
from .models import *


class TestView(APIView):
    serializer_class = TestSerializer

    @swagger_auto_schema(responses={200: serializer_class()})
    def get(self, request, pk=None, format=None):
        if pk:
            serializer = self.get_single(request, pk, format)
        else:
            serializer = self.get_many(request, format)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_single(self, request, pk, format=None):
        tests = Test.objects.get(id=pk)
        return self.serializer_class(tests)

    def get_many(self, request, format=None):
        tests = Test.objects.all()
        return self.serializer_class(tests, many=True)