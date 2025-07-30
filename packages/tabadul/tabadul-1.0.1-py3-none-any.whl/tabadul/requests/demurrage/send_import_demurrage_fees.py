class SendImportDemurrageFees:
    """
    A class to represent an API request for import demurrage fees with a complex structured JSON.
    """

    def __init__(self, data: dict):
        """
        Initialize a new instance of SendImportDemurrageFees from a structured JSON dictionary.

        :param data: The entire JSON payload as a dictionary.
        """
        # Validate and assign primary attributes based on provided data structure
        self.mode = data.get("mode")

        # Storage Identifier Information
        self.storage_identifier = data.get("storageIdentifier", {})
        self.port_code = self.storage_identifier.get("portCode")
        self.port_type = self.storage_identifier.get("portType")
        self.declaration_isn = self.storage_identifier.get("declarationISN")
        self.declaration_isn_seq = self.storage_identifier.get("declarationISNSeq")
        self.delv_isn_strg_seq = self.storage_identifier.get("delvISNStrgSeq")

        # Demurrage Fees Information
        self.demurrage_info = data.get("demurrageInfo", {})
        self.calculation_start_date = self.demurrage_info.get("calculationStartDate")
        self.calculation_end_date = self.demurrage_info.get("calculationEndDate")
        self.sys_excemptions_days = self.demurrage_info.get("sysExcemptionsDays")
        self.requested_excemptions_days = self.demurrage_info.get("requestedExcemptionsDays")
        self.vac_excemptions_days = self.demurrage_info.get("vacExcemptionsDays")
        self.total_fees = self.demurrage_info.get("totalFees")
        self.sadad_no = self.demurrage_info.get("sadadNo")

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

        # Collection Order Information
        self.col_order_info = data.get("colOrderInfo", {})
        self.collection_order_no = self.col_order_info.get("collectionOrderNo")
        self.collection_order_date = self.col_order_info.get("collectionOrderDate")
        self.collection_order_category = self.col_order_info.get("collectionOrderCategory")

    def to_dictionary(self):
        """
        Convert the instance attributes into a dictionary.

        :return: A dictionary representation of the SendImportDemurrageFees instance.
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
            "demurrageInfo": {
                "calculationStartDate": self.calculation_start_date,
                "calculationEndDate": self.calculation_end_date,
                "sysExcemptionsDays": self.sys_excemptions_days,
                "requestedExcemptionsDays": self.requested_excemptions_days,
                "vacExcemptionsDays": self.vac_excemptions_days,
                "totalFees": self.total_fees,
                "sadadNo": self.sadad_no,
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
            "colOrderInfo": {
                "collectionOrderNo": self.collection_order_no,
                "collectionOrderDate": self.collection_order_date,
                "collectionOrderCategory": self.collection_order_category,
            },
        }

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Create an instance of SendImportDemurrageFees from a dictionary based on the structured schema.

        :param dictionary: A dictionary matching the structured schema.
        :return: An instance of SendImportDemurrageFees or None if the dictionary is invalid.
        """
        if dictionary is None:
            return None
        return cls(dictionary)
