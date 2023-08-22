from django.db import models
from rest_framework import serializers

from .models import Job, JobResult


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id', 'name', 'type', 'priority', 'payload', 'time_to_reassign',
            'created_at',
        )
        read_only_fields = (
            'id', 'created_at',
        )

    def validate(self, attrs):
        jb_type = attrs.get('type')

        if jb_type == Job.Type.REST:
            payload = attrs.get('payload')
            # null payload is not allowed in REST type
            if payload is None:
                raise serializers.ValidationError("payload should not be null")
            payload_serializer = RestSerializer(data=payload)
            payload_serializer.is_valid(raise_exception=True)
            attrs['payload'] = payload_serializer.validated_data

        # Todo: add more types

        return attrs


class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = (
            'job',
            'status',
            'result',
            'content_type',
            'error',
        )


class RestSerializer(serializers.Serializer):
    class RestMethodChoices(models.TextChoices):
        GET = "GET"
        POST = "POST"
        # Todo: add more methods

    url = serializers.URLField()
    method = serializers.ChoiceField(choices=RestMethodChoices.choices)

    # headers should be string key-value pairs (dictionary)
    headers = serializers.JSONField(allow_null=True, required=False)

    # body should be validated based on the method
    # for example, if method is GET, body should be null
    # if method is POST, body should not be null
    body = serializers.JSONField(allow_null=True, required=False)

    def validate(self, attrs):
        # validate headers
        headers = attrs.get('headers')
        if headers is not None:
            if not isinstance(headers, dict):
                raise serializers.ValidationError("headers should be a dictionary")
            for key, value in headers.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise serializers.ValidationError("headers should be string key-value pairs")

        # validate method and body
        method = attrs.get('method')
        body = attrs.get('body')

        if method == self.RestMethodChoices.GET and body is not None:
            raise serializers.ValidationError("body should be null if method is GET")
        elif method == self.RestMethodChoices.POST and body is None:
            raise serializers.ValidationError("body should not be null if method is POST")

        return attrs

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError
