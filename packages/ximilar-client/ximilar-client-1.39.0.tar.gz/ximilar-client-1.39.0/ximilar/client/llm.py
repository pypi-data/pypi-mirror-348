from ximilar.client import RestClient
from ximilar.client.constants import *
from ximilar.client.constants import ENDPOINT

LLM_ENDPOINT = "llm/v2/llm"


class LLMClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, max_image_size=600, resource_name="", request_timeout=90):
        super().__init__(token, endpoint, max_image_size, resource_name, request_timeout)
        self.PREDICT_ENDPOINT = LLM_ENDPOINT

    def construct_data(self, records, **kwargs):
        if len(records) == 0:
            raise Exception("Please specify at least on record when using ocr endpoint.")

        data = {RECORDS: records}

        if kwargs:
            data.update(kwargs)

        return data

    def llm_response(self, records, lang="en", headers=None):
        """
        Call the language model endpoint.
        :param records: list of json records
        :param lang: specify the language of the text that is probably on image, defaults to "en" (currently only english is supported)
        :return: json result data from the API
        """
        data = self.construct_data(records, lang=lang)
        result = self.post(self.PREDICT_ENDPOINT, data=data, headers=headers)
        return result
