class DesFees:
    """
    This API is used to acknowledge the response from Fasah to the Bonded Area system, including details of fees.
    """

    def __init__(self, fee_details: list, is_consolidated: bool):
        """
        Initialize the acknowledgment response attributes.

        :param fee_details: A list of fee details, each containing sequence number, account number, and fee amount.
        :param is_consolidated: A boolean indicating if the fees are consolidated.
        """
        self.fee_details = fee_details
        self.is_consolidated = is_consolidated

    def to_dictionary(self):
        """
        Return the properties of the object as a dictionary.
        """
        return {
            "feeDetails": self.fee_details,
            "isConsolidated": self.is_consolidated
        }

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Creates an instance of this model from a dictionary.

        :param dictionary: A dictionary matching the structured schema.
        :return: An instance of DesFees or None if the dictionary is invalid.
        """
        if dictionary is None:
            return None

        fee_details = dictionary.get("feeDetails", [])
        is_consolidated = dictionary.get("isConsolidated", False)

        return cls(fee_details=fee_details, is_consolidated=is_consolidated)

