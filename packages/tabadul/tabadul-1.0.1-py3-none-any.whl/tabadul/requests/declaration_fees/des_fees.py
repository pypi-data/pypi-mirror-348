class DesFees:
    """
    A class to represent an API request for Declaration Fees with a complex structured JSON.
    """

    def __init__(self, data: dict):
        """
        Initialize a new instance of DesFees from a structured JSON dictionary.

        :param data: The entire JSON payload as a dictionary.
        """
        # Validate and assign primary attributes based on provided data structure
        self.decNo = data.get("decNo")

    def to_dictionary(self):
        """
        Convert the instance attributes into a dictionary.

        :return: A dictionary representation of the DesFees instance.
        """
        return {
            "decNo": self.decNo,
        }

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Create an instance of DesFees from a dictionary based on the structured schema.

        :param dictionary: A dictionary matching the structured schema.
        :return: An instance of DesFees or None if the dictionary is invalid.
        """
        if dictionary is None:
            return None
        return cls(dictionary)
