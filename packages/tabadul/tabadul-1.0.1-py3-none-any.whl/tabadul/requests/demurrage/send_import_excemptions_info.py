class SendImportExcemptionsInfo:
    """
    A class to represent an API request for import exemptions information with a complex structured JSON.
    """

    def __init__(self, data: dict):
        """
        Initialize a new instance of SendImportExcemptionsInfo from a structured JSON dictionary.

        :param data: The entire JSON payload as a dictionary.
        """
        # Primary attributes based on provided data structure
        self.mode = data.get("mode")

        # Storage Identifier Information
        self.storage_identifier = data.get("storageIdentifier", {})
        self.port_code = self.storage_identifier.get("portCode")
        self.port_type = self.storage_identifier.get("portType")
        self.declaration_isn = self.storage_identifier.get("declarationISN")
        self.declaration_isn_seq = self.storage_identifier.get("declarationISNSeq")
        self.delv_isn_strg_seq = self.storage_identifier.get("delvISNStrgSeq")

        # Exemptions Information
        self.excemptions = data.get("excemptions", {})
        self.sys_excemptions_days = self.excemptions.get("sysExcemptionsDays")
        self.requested_excemptions_days = self.excemptions.get("requestedExcemptionsDays")
        self.vac_excemptions_days = self.excemptions.get("vacExcemptionsDays")

        # Declaration Information
        self.declaration_info = data.get("declarationInfo", {})
        self.declaration_no = self.declaration_info.get("declarationNo")
        self.declaration_type = self.declaration_info.get("declarationType")
        self.declaration_date = self.declaration_info.get("declarationDate")

        # Delivery Order Information
        self.delivery_order_info = data.get("deliveryOrderInfo", {})
        self.shipping_agent_no = self.delivery_order_info.get("shippingAgentNo")
        self.delivery_order_no = self.delivery_order_info.get("deliveryOrderNo")
        self.delivery_date = self.delivery_order_info.get("deliveryDate")

    def to_dictionary(self):
        """
        Convert the instance attributes into a dictionary.

        :return: A dictionary representation of the SendImportExcemptionsInfo instance.
        """
        return {
            "mode": self.mode,
            "storageIdentifier": {
                "portCode": self.port_code,
                "portType": self.port_type,
                "declarationISN": self.declaration_isn,
                "declarationISNSeq": self.declaration_isn_seq,
                "delvISNStrgSeq": self.delv_isn_strg_seq,
            },
            "excemptions": {
                "sysExcemptionsDays": self.sys_excemptions_days,
                "requestedExcemptionsDays": self.requested_excemptions_days,
                "vacExcemptionsDays": self.vac_excemptions_days,
            },
            "declarationInfo": {
                "declarationNo": self.declaration_no,
                "declarationType": self.declaration_type,
                "declarationDate": self.declaration_date,
            },
            "deliveryOrderInfo": {
                "shippingAgentNo": self.shipping_agent_no,
                "deliveryOrderNo": self.delivery_order_no,
                "deliveryDate": self.delivery_date,
            },
        }

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Create an instance of SendImportExcemptionsInfo from a dictionary based on the structured schema.

        :param dictionary: A dictionary matching the structured schema.
        :return: An instance of SendImportExcemptionsInfo or None if the dictionary is invalid.
        """
        if dictionary is None:
            return None
        return cls(dictionary)