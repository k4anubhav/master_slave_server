import uuid

from django.db import models


class Slave(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.CharField(max_length=100, unique=True)

    last_seen = models.DateTimeField(auto_now_add=True)  # not updated on every save

    notification_token = models.TextField(max_length=400, blank=True, null=True)


class SlaveToken(models.Model):
    slave = models.OneToOneField(Slave, on_delete=models.CASCADE, related_name="token")
    token = models.CharField(max_length=40, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return uuid.uuid4().hex

    def __str__(self):
        return self.token
