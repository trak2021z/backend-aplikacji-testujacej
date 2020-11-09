from django.shortcuts import render

# Create your views here.
from drf_yasg2.utils import swagger_auto_schema, is_list_view
from rest_framework.response import Response
from rest_framework import status, serializers, viewsets
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Count
import json
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from .serializers import *
from .models import *


class TestView(APIView):
    testSerializer = TestSerializer
    testDetailsSerializer = TestDetailsSerializer

    @swagger_auto_schema(responses={200: testSerializer()})
    def get(self, request, pk=None, format=None):
        if pk:
            serializer = self.get_single(request, pk, format)
        else:
            serializer = self.get_many(request, format)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_single(self, request, pk, format=None):
        tests = Test.objects.get(id=pk)
        ids = list(TestEndpoint.objects.values().filter(test_id=pk).values_list('endpoint_id', flat=True))
        endpoints = list(Endpoint.objects.values().filter(id__in=ids))
        return self.testDetailsSerializer(tests, context={'endpoints': endpoints})

    def get_many(self, request, format=None):
        tests = Test.objects.all()
        return self.testSerializer(tests, many=True)

class ResultView(APIView):
    testResultsSerializer = TestResultsSerializer
    @swagger_auto_schema(responses={200: testResultsSerializer()})

    def get(self, request, pk=None, format=None):
        if pk:
            serializer = self.get_single(request, pk, format).data
        else:
            serializer = self.get_many(request, format)
        return Response(serializer, status=status.HTTP_200_OK)

    def get_single(self, request, pk, format=None):
        tests = Test.objects.get(id=pk)
        testCall_ids = list(TestCall.objects.values().filter(test_id=pk).values_list('id', flat=True))
        testCalls = list(TestCall.objects
        .values('id', 'start_date', 'end_date', 'num_users', 'is_finished', 'is_finished')
        .filter(id__in = testCall_ids).order_by('-start_date'))

        for testCall in testCalls:
            testCall['results'] = list(Result.objects.values('results')
                                       .filter(test_call_id = testCall['id'])
                                       .values_list('results', flat=True))
        return self.testResultsSerializer(tests, context={'testCalls': testCalls})

    def get_many(self, request, format=None):
        result = []
        tests = list(Test.objects.values())
        for test in tests:
            testCall_ids = list(TestCall.objects.values().filter(test_id=test['id']).values_list('id', flat=True))
            testCalls = list(TestCall.objects
            .values('id', 'start_date', 'end_date', 'num_users', 'is_finished', 'is_finished')
            .filter(id__in = testCall_ids).order_by('-start_date'))
            for testCall in testCalls:
                testCall['results'] = list(Result.objects.values('results')
                                           .filter(test_call_id = testCall['id'])
                                           .values_list('results', flat=True))
            result.append(self.testResultsSerializer(test, context={'testCalls': testCalls}).data)


        return result

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