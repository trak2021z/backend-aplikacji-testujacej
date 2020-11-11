from django.shortcuts import render

# Create your views here.
from drf_yasg2.openapi import Parameter
from drf_yasg2.utils import swagger_auto_schema, is_list_view
from rest_framework.permissions import BasePermission
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

    @swagger_auto_schema(responses={200: testSerializer()},
                         manual_parameters=[Parameter(name="FRONT", in_='header', type='str')])
    def get(self, request, pk=None, format=None):
        if pk:
            serializer = self.get_single(request, pk, format).data
        else:
            serializer = self.get_many(request, format)
        return Response(serializer, status=status.HTTP_200_OK)

    def get_single(self, request, pk, format=None):
        tests = Test.objects.get(id=pk)
        ids = list(TestEndpoint.objects.values().filter(test_id=pk).values_list('endpoint_id', flat=True))
        endpoints = list(Endpoint.objects.values().filter(id__in=ids))
        for endpoint in endpoints:
            endpoint['order'] = TestEndpoint.objects.filter(test_id=pk).filter(endpoint_id=endpoint['id']).values(
                'order').values_list('order', flat=True)
        return self.testDetailsSerializer(tests, context={'endpoints': endpoints})

    def get_many(self, request, format=None):
        result = []
        tests = list(Test.objects.values())
        for test in tests:
            endpoints_count = TestEndpoint.objects.filter(test_id=test['id']).count()
            result.append(self.testSerializer(test, context={'endpoints_count': endpoints_count}).data)
        return result


class ResultView(APIView):
    testResultsSerializer = TestResultsSerializer

    @swagger_auto_schema(responses={200: testResultsSerializer()},
                         manual_parameters=[Parameter(name="FRONT", in_='header', type='str')])
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
                         .filter(id__in=testCall_ids).order_by('-start_date'))

        for testCall in testCalls:
            results = list(Result.objects.values('results')
                           .filter(test_call_id=testCall['id'])
                           .values_list('results', flat=True))
            json_results = []
            for result_str in results:
                json_results.append(json.loads(result_str))
            testCall['results'] = json_results
        return self.testResultsSerializer(tests, context={'testCalls': testCalls})

    def get_many(self, request, format=None):
        result = []
        tests = list(Test.objects.values())
        for test in tests:
            testCall_ids = list(TestCall.objects.values().filter(test_id=test['id']).values_list('id', flat=True))
            testCalls = list(TestCall.objects
                             .values('id', 'start_date', 'end_date', 'num_users', 'is_finished', 'is_finished')
                             .filter(id__in=testCall_ids).order_by('-start_date'))
            for testCall in testCalls:
                results = list(Result.objects.values('results')
                               .filter(test_call_id=testCall['id'])
                               .values_list('results', flat=True))
                json_results = []
                for result_str in results:
                    json_results.append(json.loads(result_str))
                testCall['results'] = json_results
            result.append(self.testResultsSerializer(test, context={'testCalls': testCalls}).data)
        return result


class TestCallView(APIView):
    serializer_class = TestCallSerializer

    @swagger_auto_schema(responses={200: serializer_class()},
                         manual_parameters=[Parameter(name="FRONT", in_='header', type='str')])
    def get(self, request, pk=None, format=None):
        if pk:
            try:
                test_call = TestCall.objects.get(id=pk)
                serializer = self.serializer_class(test_call)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Result.DoesNotExist:
                return Response({'error': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            test_calls = TestCall.objects.all()
            serializer = self.serializer_class(test_calls, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TestCallInputSerializer(data=request.data, fields=('test', 'num_users', 'max_calls'))
        if serializer.is_valid():
            test_id = serializer.validated_data['test']
            try:
                test_call = TestCall.objects.create(
                    test=test_id,
                    num_users=serializer.validated_data["num_users"],
                    max_calls=serializer.validated_data["max_calls"]
                )
                save_serializer = TestCallSerializer(test_call)
                return Response(save_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestCallDetailsView(APIView):
    serializer_class = TestCallDetailsSerializer

    @swagger_auto_schema(responses={200: serializer_class()},
                         manual_parameters=[Parameter(name="FRONT", in_='header', type='str')])
    def get(self, request, pk=None, format=None):
        if pk:
            try:
                test_call = TestCall.objects.get(id=pk)
                serializer = self.serializer_class(test_call)
                data = serializer.data
                results = Result.objects.filter(test_call=test_call)
                json_results = []
                for result in results:
                    json_results.append(json.loads(result.results))
                data["results"] = json_results
                return Response(data, status=status.HTTP_200_OK)
            except Result.DoesNotExist:
                return Response({'error': 'Test Call not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'No pk specified'}, status=status.HTTP_404_NOT_FOUND)


class TestCallByDateView(APIView):
    serializer_class = TestCallSerializer

    @swagger_auto_schema(responses={200: serializer_class()},
                         manual_parameters=[Parameter(name="FRONT", in_='header', type='str')])
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

    def get_many(self, request, date, format=None):
        test_calls = TestCall.objects.filter(start_date__date=date.date())
        serializer = self.serializer_class(test_calls, many=True)
        return serializer.data
