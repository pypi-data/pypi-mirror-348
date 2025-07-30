import json
from urllib.parse import urlencode

from tabadul.configuration import Configuration
from tabadul.exceptions.api_exception import APIException
from tabadul.helpers.api_helper import APIHelper
from tabadul.http.auth.api_token import APITokenAuthentication
from tabadul.http.http_context import HttpContext
from tabadul.http.requests_client import RequestsClient


class Handler(object):
    """
    All handlers inherit from this base class.
    """

    path = ''
    authentication_model = APITokenAuthentication

    def __init__(self, client=None):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        self.global_headers = {'Content-Type': 'application/json'}
        self.base_url = Configuration.get_base_uri(Configuration.Server.BASE_URL)
        self.http_client = client if client else RequestsClient()

    def validate_response(self, context):
        """
        Validates an HTTP response by checking for global errors.
        """
        print(context.response.raw_body)

        if context.response.status_code == 404:
            raise APIException('Page not Found', context)
        if context.response.status_code == 401:
            raise APIException('Authentication failed', context)
        elif context.response.status_code == 406:
            raise APIException('Wrong parameter format', context)
        elif context.response.status_code == 449:
            raise APIException('Message body is empty', context)
        elif context.response.status_code == 451:
            raise APIException('TimeScheduled parameter must indicate time in the future', context)
        elif context.response.status_code == 480:
            raise APIException('This user cannot use specified SenderID', context)
        elif context.response.status_code == 482:
            raise APIException('Invalid dest num', context)
        elif context.response.status_code < 200 or context.response.status_code > 208:
            raise APIException('HTTP response not OK.', context)

        return context

    def execute_request(self, request):
        """
        Executes an HttpRequest with query parameters.
        """
        # Combine base URL and query URL
        request.query_url = self.base_url + request.query_url

        # Add query parameters to the URL, if any are provided
        if hasattr(request, 'query_parameters') and request.query_parameters:
            query_string = urlencode(request.query_parameters)
            request.query_url += '?' + query_string

        # Merge headers and parameters, and authenticate the request
        request.headers = APIHelper.merge_dicts(self.global_headers, request.headers)

        # Add  parameters to the Body, if any are provided
        if hasattr(request, 'parameters') and request.parameters:
            request.parameters = json.dumps(request.parameters)

        self.authentication_model.apply(request)

        # Execute the HTTP request
        response = self.http_client.execute(request)
        context = HttpContext(request, response)

        # Validate the response
        self.validate_response(context)

        return context
