import logging

import requests
from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response

from slave.permissions import IsSlaveAuthenticated
from .models import Job, JobLock
from .serializers import JobSerializer, JobResultSerializer

WEBHOOK_URL = settings.WEBHOOK_URL

logger = logging.getLogger(__name__)


class CreateJobView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )


class GetJobAssignedView(generics.RetrieveAPIView):
    serializer_class = JobSerializer
    permission_classes = (
        IsSlaveAuthenticated,
    )

    def get_queryset(self):
        crt_time = timezone.now()
        return (
            Job
            .objects
            .annotate_status()
            .filter(Q(status='PENDING'))
            .filter(Q(lock__isnull=True) | Q(lock__till__lt=crt_time))
            .order_by('-priority', 'created_at')
        )

    def get_object(self):
        queryset = self.get_queryset()
        job: 'Job' = queryset.first()
        if job is None:
            raise Http404

        # lock the job
        crt_time = timezone.now()
        JobLock.objects.update_or_create(
            job_id=job.id,
            defaults={
                'created_at': crt_time,
                'till': crt_time + timezone.timedelta(seconds=job.time_to_reassign),
                'lock_to': self.request.slave,
            }
        )

        return job


class CreateJobResultView(generics.CreateAPIView):
    serializer_class = JobResultSerializer
    permission_classes = (
        IsSlaveAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # TODO: add signature
        # TODO: move to another process - blocking webserver
        try:
            if WEBHOOK_URL:
                requests.post(WEBHOOK_URL, json=response.data, timeout=5)
        except Exception as e:
            logger.error(e)
        return response


class PingView(generics.GenericAPIView):
    permission_classes = (
        IsSlaveAuthenticated,
    )

    @staticmethod
    def get(request, *args, **kwargs):
        return Response({'status': 'ok'})
