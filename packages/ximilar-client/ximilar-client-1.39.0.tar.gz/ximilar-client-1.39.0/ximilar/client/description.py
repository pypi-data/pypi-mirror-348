from ximilar.client import RestClient
from ximilar.client.constants import *

PRODUCT_ENDPOINT = "product-description/v2/generate"


class ProductDescriptionClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, resource_name="product-description"):
        super().__init__(token=token, endpoint=endpoint, resource_name=resource_name)
        self.PREDICT_ENDPOINT = PRODUCT_ENDPOINT

    def construct_data(self, records=[], style_name=None, product_info=None, product_type=None, tagging_type=None):
        if len(records) == 0:
            raise Exception("Please specify at least one record in detect method!")
        data = {RECORDS: self.preprocess_records(records)}

        if style_name:
            data["style_name"] = style_name
        if product_info:
            data["product_info"] = product_info
        if product_type:
            data["product_type"] = product_type
        if tagging_type:
            data["tagging_type"] = tagging_type

        return data

    def generate(self, records, style_name=None, product_info=None, product_type=None, tagging_type=None):
        records = self.preprocess_records(records)
        return self.post(
            PRODUCT_ENDPOINT, data=self.construct_data(records, style_name, product_info, product_type, tagging_type)
        )
