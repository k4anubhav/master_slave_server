import uuid

from django.core.validators import MinValueValidator
from django.db import models


class JobQuerySet(models.QuerySet):
    def annotate_status(self):
        return self.annotate(
            status=models.Case(
                models.When(result__status=JobResult.Status.SUCCESS, then=models.Value('SUCCESS')),
                models.When(result__status=JobResult.Status.FAILURE, then=models.Value('FAILURE')),
                default=models.Value('PENDING'),
            )
        )


class Job(models.Model):
    class Type(models.TextChoices):
        REST = "REST"

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, choices=Type.choices)

    priority = models.IntegerField(default=5, validators=[MinValueValidator(0)])
    payload = models.JSONField(blank=True, null=True)
    time_to_reassign = models.IntegerField(default=10, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True)

    objects = JobQuerySet.as_manager()

    def __str__(self):
        return f'{self.id} - {self.name}'

    class Meta:
        db_table = "job_queue"
        verbose_name = "Job Queue"
        verbose_name_plural = "Job Queue"
        ordering = ["-created_at"]


class JobResult(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS"
        FAILURE = "FAILURE"

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="result")
    status = models.CharField(max_length=100, choices=Status.choices)
    result = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.status}'

    class Meta:
        db_table = "job_result"
        verbose_name = "Job Result"
        verbose_name_plural = "Job Result"
        ordering = ["-created_at"]


# Not using cache for lock as of now
class JobLock(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="lock")
    lock_to = models.ForeignKey('slave.Slave', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    till = models.DateTimeField()

    def __str__(self):
        return f'{self.id} - {self.job}'

    class Meta:
        db_table = "job_lock"
        verbose_name = "Job Lock"
        verbose_name_plural = "Job Lock"
        ordering = ["-created_at"]
