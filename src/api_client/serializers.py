from rest_framework import serializers
from .models import Test,TestCall,Result,Endpoint,TestEndpoint



class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class TestSerializer(DynamicFieldsModelSerializer):
    endpoints_count = serializers.SerializerMethodField()
    
    def get_endpoints_count(self, obj):
        endpoints_count = self.context.get('endpoints_count')
        return endpoints_count
        
    class Meta:
        model = Test
        fields = ('id', 'name', 'description', 'endpoints_count')
        
        

class EndpointSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Endpoint
        fields = ('url', 'name', 'request', 'test_endpoints' )


class TestDetailsSerializer(DynamicFieldsModelSerializer):
    endpoints = serializers.SerializerMethodField()

    def get_endpoints(self, obj):
        endpoints = self.context.get('endpoints')
        return endpoints

    class Meta:
        model = Test
        fields = ('name', 'description', 'endpoints')

class TestCallSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestCall
        fields = ('id', 'start_date', 'end_date', 'num_users', 'max_calls', 'is_finished')

class TestCallInputSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = TestCall
        fields = ['test', 'num_users', 'max_calls']

class ResultSerializer(DynamicFieldsModelSerializer):
    test_call = TestCallSerializer()
    class Meta:
        model = Result
        fields = ('test_call', 'results')

class TestResultsSerializer(DynamicFieldsModelSerializer):
    testCalls = serializers.SerializerMethodField()

    def get_testCalls(self, obj):
        testCalls = self.context.get('testCalls')
        return testCalls

    class Meta:
        model = Test
        fields = ('name', 'description', 'testCalls')

class TestCallDetailsSerializer(DynamicFieldsModelSerializer):
    test = TestDetailsSerializer()
    results = serializers.SerializerMethodField()

    def get_results(self, obj):
        results = self.context.get('results')
        return results

    class Meta:
        model = TestCall
        fields = ('id', 'test', 'start_date', 'end_date', 'num_users', 'max_calls', 'is_finished', 'results')