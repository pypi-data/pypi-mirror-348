from tabadul.configuration import Configuration
from tabadul.requests.demurrage.send_import_demurrage_fees import SendImportDemurrageFees
from tabadul.handlers.demurrage.send_import_demurrage_fees import send_import_demurrage_fees_handler
from tabadul.requests.demurrage.send_transhipment_demurrage_fees import SendTranshipmentDemurrageFees
from tabadul.handlers.demurrage.send_transhipment_demurrage_fees import send_transhipment_demurrage_fees_handler
from tabadul.requests.declaration_fees.des_fees import DesFees
from tabadul.handlers.declaration_fees.des_fees import des_fees_handler


class TabadulClient(object):
    """
    A client for interacting with the Tabadul API.
    """
    config = Configuration

    def __init__(self, tabadul_client_id, tabadul_client_secret):
        """
        Initializes the TabadulClient with the necessary credentials.

        :param tabadul_client_id: The client ID for API authentication.
        :param tabadul_client_secret: The client secret key for API authentication.
        """
        Configuration.tabadul_client_id = tabadul_client_id
        Configuration.tabadul_client_secret = tabadul_client_secret

    def send_import_demurrage_fees(self, data: dict):
        """
        Sends import demurrage fees data to the Bonded Area system.

        :param data: A dictionary containing the request parameters, including all required fields.

        :return: An HTTP response. On success, it returns status 200 with the result in the response body as JSON.
                 On failure, returns an HTTP error response with a JSON body containing an error code and description.
        """
        return send_import_demurrage_fees_handler(request=SendImportDemurrageFees(data))

    def send_transhipment_demurrage_fees(self, data: dict):
        """
        Sends transshipment demurrage fees data to the bonded area system.

        :param data: A dictionary containing the request parameters, including all required fields.

        :return: The API response. On success, returns a 200 status with the result in JSON format in the response body.
                 On failure, returns an HTTP error response with a JSON body containing an error code and description.
        """
        return send_transhipment_demurrage_fees_handler(request=SendTranshipmentDemurrageFees(data))

    def des_fees(self, data: dict):
        """
        Sends declaration fees data to the bonded area system.

        :param data: A dictionary containing the request parameters, including all required fields for the API.

        :return: The API response. On success, returns a response with status 200 and the result in JSON format.
                 On failure, returns an HTTP error response with a JSON body containing an error code and description.
        """
        return des_fees_handler(request=DesFees(data))
