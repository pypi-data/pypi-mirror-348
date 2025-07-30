class SendTranshipmentDemurrageFees:
    """
    A class to represent an API request for transshipment demurrage fees with a complex structured JSON.
    """

    def __init__(self, data: dict):
        """
        Initialize a new instance of SendTranshipmentDemurrageFees from a structured JSON dictionary.

        :param data: The entire JSON payload as a dictionary.
        """
        # Primary attribute
        self.mode = data.get("mode")

        # Bill Information
        self.bill_info = data.get("billInfo", {})
        self.port_code = self.bill_info.get("portCode")
        self.port_type = self.bill_info.get("portType")
        self.shipping_agent_no = self.bill_info.get("shippingAgentNo")
        self.cntnr_count = self.bill_info.get("cntnrCount")
        self.imp_bl_seq_no = self.bill_info.get("impBlSeqNo")
        self.imp_manifest_issued_date = self.bill_info.get("impManifestIssuedDate")
        self.imp_manifest_no = self.bill_info.get("impManifestNo")
        self.imp_manifest_type = self.bill_info.get("impManifestType")
        self.exp_manifest_type = self.bill_info.get("expManifestType")
        self.exp_manifest_no = self.bill_info.get("expManifestNo")
        self.exp_manifest_issued_date = self.bill_info.get("expManifestIssuedDate")
        self.exp_bl_seq_no = self.bill_info.get("expBlSeqNo")

        # Collection Order Information
        self.col_order_info = data.get("colOrderInfo", {})
        self.collection_order_no = self.col_order_info.get("collectionOrderNo")
        self.collection_order_date = self.col_order_info.get("collectionOrderDate")
        self.collection_order_category = self.col_order_info.get("collectionOrderCategory")

        # Demurrage Fees Information
        self.demurrage_info = data.get("demurrageInfo", {})
        self.calculation_start_date = self.demurrage_info.get("calculationStartDate")
        self.calculation_end_date = self.demurrage_info.get("calculationEndDate")
        self.sys_excemptions_days = self.demurrage_info.get("sysExcemptionsDays")
        self.requested_excemptions_days = self.demurrage_info.get("requestedExcemptionsDays")
        self.vac_excemptions_days = self.demurrage_info.get("vacExcemptionsDays")
        self.total_fees = self.demurrage_info.get("totalFees")
        self.sadad_no = self.demurrage_info.get("sadadNo")

        # Load Permit Information
        self.load_permit_info = data.get("loadPermitInfo", {})
        self.permit_date = self.load_permit_info.get("permitDate")
        self.permit_no = self.load_permit_info.get("permitNo")
        self.arrival_country = self.load_permit_info.get("arrivalCountry")
        self.arrival_port_type = self.load_permit_info.get("arrivalPortType")
        self.arrival_port_code = self.load_permit_info.get("arrivalPortCode")
        self.permit_status = self.load_permit_info.get("permitStatus")

    def to_dictionary(self):
        """
        Convert the instance attributes into a dictionary.

        :return: A dictionary representation of the SendTranshipmentDemurrageFees instance.
        """
        return {
            "mode": self.mode,
            "billInfo": {
                "portCode": self.port_code,
                "portType": self.port_type,
                "shippingAgentNo": self.shipping_agent_no,
                "cntnrCount": self.cntnr_count,
                "impBlSeqNo": self.imp_bl_seq_no,
                "impManifestIssuedDate": self.imp_manifest_issued_date,
                "impManifestNo": self.imp_manifest_no,
                "impManifestType": self.imp_manifest_type,
                "expManifestType": self.exp_manifest_type,
                "expManifestNo": self.exp_manifest_no,
                "expManifestIssuedDate": self.exp_manifest_issued_date,
                "expBlSeqNo": self.exp_bl_seq_no,
            },
            "colOrderInfo": {
                "collectionOrderNo": self.collection_order_no,
                "collectionOrderDate": self.collection_order_date,
                "collectionOrderCategory": self.collection_order_category,
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
            "loadPermitInfo": {
                "permitDate": self.permit_date,
                "permitNo": self.permit_no,
                "arrivalCountry": self.arrival_country,
                "arrivalPortType": self.arrival_port_type,
                "arrivalPortCode": self.arrival_port_code,
                "permitStatus": self.permit_status,
            },
        }

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Create an instance of SendTranshipmentDemurrageFees from a dictionary based on the structured schema.

        :param dictionary: A dictionary matching the structured schema.
        :return: An instance of SendTranshipmentDemurrageFees or None if the dictionary is invalid.
        """
        if dictionary is None:
            return None
        return cls(dictionary)
