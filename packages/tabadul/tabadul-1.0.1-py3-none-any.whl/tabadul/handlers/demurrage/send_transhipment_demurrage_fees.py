from tabadul.handlers.handler import Handler
from tabadul.helpers.api_helper import APIHelper
from tabadul.responses.demurrage import send_transhipment_demurrage_fees as response
from tabadul.requests.demurrage import send_transhipment_demurrage_fees as requests


class SendTranshipmentDemurrageFeesHandler(Handler):
    """
    Handles the API call to send transshipment demurrage fees data to the bonded area system.
    """

    path = '/tabadul/qa/demurrage/v2/api/sendTranshipmentDemurrageFees'
    response_model = response.SendTransshipmentDemurrageFeesResponse

    def __call__(self, request: requests.SendTranshipmentDemurrageFees):
        """
        Executes an API call to send transshipment demurrage fees data and returns an instance of the response model.

        :param request: An instance of SendTranshipmentDemurrageFees request model.
        :return: An instance of SendTransshipmentDemurrageFeesResponse containing the API response data.
        """
        parameters = request.to_dictionary()
        request = self.http_client.post(self.path, parameters=parameters)
        context = self.execute_request(request)
        return APIHelper.json_deserialize(context.response.raw_body, self.response_model.from_dictionary)


send_transhipment_demurrage_fees_handler = SendTranshipmentDemurrageFeesHandler()