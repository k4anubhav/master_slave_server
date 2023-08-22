from rest_framework import status, permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Slave, SlaveToken
from .serializers import SlaveTokenSerializer, SlaveUsernameSerializer, SlaveUsernameWithoutUniqueSerializer


class SlaveViewSet(viewsets.ViewSet):
    permission_classes = (
        permissions.IsAdminUser,
    )

    @staticmethod
    def get_username(request: Request):
        serializer = SlaveUsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return data['username']

    @staticmethod
    def get_username_without_unique(request: Request):
        serializer = SlaveUsernameWithoutUniqueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return data['username']

    def create(self, request: Request, *args, **kwargs) -> Response:
        username = self.get_username(request)

        try:
            slave = Slave.objects.get(username=username)
        except Slave.DoesNotExist:
            slave = Slave.objects.create(username=username)

        token = SlaveToken.objects.create(slave=slave)

        serializer = SlaveTokenSerializer(token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def regenerate(self, request: Request, *args, **kwargs) -> Response:
        username = self.get_username_without_unique(request)

        slave = Slave.objects.get(username=username)

        slave.token.delete()
        token = SlaveToken.objects.create(slave=slave)
        serializer = SlaveTokenSerializer(token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
