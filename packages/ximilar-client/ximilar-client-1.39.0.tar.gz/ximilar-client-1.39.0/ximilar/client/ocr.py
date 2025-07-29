import requests

from ximilar.client import RestClient
from ximilar.client.constants import *

READ_ENDPOINT = "ocr/v2/read"
READ_GPT_ENDPOINT = "ocr/v2/read_gpt"


class OCRClient(RestClient):
    def construct_data(self, records, **kwargs):
        if len(records) == 0:
            raise Exception("Please specify at least on record when using ocr endpoint.")

        data = {RECORDS: self.preprocess_records(records)}

        if kwargs:
            data.update(kwargs)

        return data

    def read(self, records, lang="en", **kwargs):
        """
        Call the ocr endpoint.
        :param records: list of json records
        :param lang: specify the language of the text that is probably on image, defaults to "en"
        :return: json result data from the API
        """
        data = self.construct_data(records, lang=lang, **kwargs)
        result = self.post(READ_ENDPOINT, data=data)
        return result

    def read_gpt(self, records, lang="en", **kwargs):
        """
        Call the ocr + gpt endpoint.
        :param records: list of json records
        :param lang: specify the language of the text that is probably on image, defaults to "en"
        :return: json result data from the API
        """
        data = self.construct_data(records, lang=lang, **kwargs)
        result = self.post(READ_GPT_ENDPOINT, data=data)
        return result


if __name__ == "__main__":
    import sys

    client = OCRClient(sys.argv[1])
    print(client.read([{"_url": "https://images.ximilar.com/examples/cards/mew_pokemon.jpeg"}]))
    print(
        client.read_gpt(
            [
                {
                    "_url": "https://images.ximilar.com/examples/cards/mew_pokemon.jpeg",
                    "prompt": "based on the following result from ocr system what is the name and type of the card as json result ({'name':'', 'type': ''})",
                }
            ]
        )
    )
