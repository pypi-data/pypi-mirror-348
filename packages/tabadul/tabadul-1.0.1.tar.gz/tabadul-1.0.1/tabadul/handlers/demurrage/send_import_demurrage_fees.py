from tabadul.handlers.handler import Handler
from tabadul.helpers.api_helper import APIHelper
from tabadul.responses.demurrage import send_import_demurrage_fees as response
from tabadul.requests.demurrage import send_import_demurrage_fees as requests


class SendImportDemurrageFeesHandler(Handler):
    """
    This API is used to send import demurrage fees data to the bonded area system.
    """

    path = '/tabadul/qa/demurrage/v2/api/sendImportDemurrageFees'
    response_model = response.SendImportDemurrageFeesResponse

    def __call__(self, request: requests.SendImportDemurrageFees):
        """
        Calls the API to send import demurrage fees data and returns a response model instance.
        """
        parameters = request.to_dictionary()
        request = self.http_client.post(self.path, parameters=parameters)
        context = self.execute_request(request)
        return APIHelper.json_deserialize(context.response.raw_body, self.response_model.from_dictionary)


send_import_demurrage_fees_handler = SendImportDemurrageFeesHandler()
