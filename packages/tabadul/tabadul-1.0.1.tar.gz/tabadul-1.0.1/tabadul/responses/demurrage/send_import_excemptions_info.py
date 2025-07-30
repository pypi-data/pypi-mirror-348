class SendImportExemptionsInfo:
    """
    This API is used to acknowledge the response from Fasah to the Bonded Area system regarding import exemptions.
    """

    def __init__(self, status_code: str, status_description: str, transaction_id: str):
        """
        Initialize the acknowledgment response attributes.

        :param status_code: Invocation status code (Standard HTTP Codes)
        :param status_description: Description of the invocation status
        :param transaction_id: Transaction ID sent in the request
        """
        self.status = {
            "statusCode": status_code,
            "statusDescription": status_description,
            "transactionId": transaction_id
        }

    def to_dictionary(self):
        """
        Return the properties of the object as a dictionary.
        """
        return {
            "status": self.status
        }

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Creates an instance of this model from a dictionary.

        :param dictionary: A dictionary matching the structured schema.
        :return: An instance of SendImportExemptionsInfo or None if the dictionary is invalid.
        """
        if dictionary is None:
            return None

        status = dictionary.get("status", {})
        status_code = status.get("statusCode")
        status_description = status.get("statusDescription")
        transaction_id = status.get("transactionId")

        return cls(status_code=status_code, status_description=status_description, transaction_id=transaction_id)