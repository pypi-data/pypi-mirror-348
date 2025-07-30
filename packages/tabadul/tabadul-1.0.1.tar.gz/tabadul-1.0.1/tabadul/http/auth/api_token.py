import uuid
from tabadul.configuration import Configuration


class APITokenAuthentication(object):

    @staticmethod
    def apply(http_request):
        """
        Add token authentication to the header request.
        Args:
            http_request (HttpRequest): The HttpRequest object to which authentication will be added.
        """
        http_request.headers["X-Tabadul-Client-Id"] = Configuration.tabadul_client_id
        http_request.headers["X-Tabadul-Client-Secret"] = Configuration.tabadul_client_secret
        http_request.headers["transactionId"] = f'{int(uuid.uuid4().hex, 16)}'
