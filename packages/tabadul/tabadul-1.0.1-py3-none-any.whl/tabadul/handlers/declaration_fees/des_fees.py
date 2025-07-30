from tabadul.handlers.handler import Handler
from tabadul.helpers.api_helper import APIHelper
from tabadul.responses.declaration_fees import des_fees as response
from tabadul.requests.declaration_fees import des_fees as requests


class DesFeesHandler(Handler):
    """
    This handler is used to send declaration fees data to the bonded area system.
    """

    path = '/tabadul/qa/declarationFees/api/v1/desFees'
    response_model = response.DesFees

    def __call__(self, request: requests.DesFees):
        """
        Sends the declaration fees data to the API and returns a response model instance.

        :param request: An instance of the DesFees request model containing the fees data.
        :return: A response model instance with the API response data.
        """
        parameters = request.to_dictionary()
        request = self.http_client.get(self.path, query_parameters=parameters)
        context = self.execute_request(request)
        return APIHelper.json_deserialize(context.response.raw_body, self.response_model.from_dictionary)


des_fees_handler = DesFeesHandler()
