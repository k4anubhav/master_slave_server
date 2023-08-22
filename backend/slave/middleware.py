from .models import Slave


class AuthSlaveMiddleware:
    KEYWORD = 'Slave'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.slave = self.get_slave(request)
        return self.get_response(request)

    @staticmethod
    def get_slave(request):
        token = request.META.get('HTTP_SLAVE_AUTH', None)
        if token is None:
            return None

        if token.lower().startswith(f'{AuthSlaveMiddleware.KEYWORD.lower()} '):
            token = token[6:]
        else:
            return None

        try:
            return Slave.objects.get(
                token__token=token,
            )
        except Slave.DoesNotExist:
            return None
