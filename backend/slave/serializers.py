from rest_framework import serializers

from .models import Slave, SlaveToken


class SlaveUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slave
        fields = (
            'username',
        )


class SlaveUsernameWithoutUniqueSerializer(SlaveUsernameSerializer):
    class Meta(SlaveUsernameSerializer.Meta):
        extra_kwargs = {
            'username': {'validators': []},
        }


class SlaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slave
        fields = (
            'id', 'username', 'last_seen', 'notification_token'
        )
        read_only_fields = (
            'id', 'last_seen'
        )


class SlaveTokenSerializer(serializers.ModelSerializer):
    slave_username = serializers.CharField(source='slave.username', read_only=True)

    class Meta:
        model = SlaveToken
        fields = (
            'slave_id', 'slave_username', 'token'
        )
