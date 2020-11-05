from django.shortcuts import render

# Create your views here.
from drf_yasg2.utils import swagger_auto_schema, is_list_view
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from datetime import datetime
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

class TestResultView(APIView):
    serializer_class = TestResultSerializer

    def get(self, request, pk=None, format=None):
        if pk:
            try:
                result = Result.objects.get(id=pk)
                serializer = self.serializer_class(result)
                data = serializer.data
                data["results"] = json.loads(data["results"])
                return Response(data, status=status.HTTP_200_OK)
            except Result.DoesNotExist:
                return Response({'error': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'No pk specified'}, status=status.HTTP_404_NOT_FOUND)

class TestResultByDateView(APIView):
    serializer_class = TestResultSerializer
    def get(self, request, test_date=None, format=None):
        if test_date:
            try:
                date = datetime.strptime(test_date, '%d-%m-%Y')
            except ValueError as e:
                return Response({'error': 'Wrong date format! Use \'dd-mm-yyyy\'.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            date = datetime.now()
        data = self.get_many(request, date, format)
        return Response(data, status=status.HTTP_200_OK)
    def get_many(self, request,  date, format=None):
        test_calls = TestCall.objects.filter(start_date__date=date.date())
        tests = Result.objects.filter(test_call__in=test_calls)
        serializer = self.serializer_class(tests, many=True)
        data = serializer.data
        for result in data:
            result['results'] = json.loads(result['results'])
        return data