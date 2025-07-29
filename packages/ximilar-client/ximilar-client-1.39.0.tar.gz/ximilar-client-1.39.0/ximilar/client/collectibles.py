from ximilar.client import RestClient
from ximilar.client.constants import *

GRADING_ENDPOINT = "card-grader/v2/grade"
CONDITION_ENDPOINT = "card-grader/v2/condition"
CENTERING_ENDPOINT = "card-grader/v2/centering"

COLLECTIBLES_PROCESS = "collectibles/v2/process"
COLLECTIBLES_COMICS_ID = "collectibles/v2/comics_id"
COLLECTIBLES_CARD_ID = "collectibles/v2/tcg_id"
COLLECTIBLES_SPORT_ID = "collectibles/v2/sport_id"
COLLECTIBLES_DETECT = "collectibles/v2/detect"
COLLECTIBLES_SLAB_ID = "collectibles/v2/slab_id"
COLLECTIBLES_OCR_ID = "collectibles/v2/ocr_id"
COLLECTIBLES_ANALYZE = "collectibles/v2/analyze"


class CardGradingClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, resource_name="card-grader"):
        super().__init__(token=token, endpoint=endpoint, resource_name=resource_name)
        self.PREDICT_ENDPOINT = GRADING_ENDPOINT

    def construct_data(self, records=[]):
        if len(records) == 0:
            raise Exception("Please specify at least one record in detect method!")
        data = {RECORDS: self.preprocess_records(records)}
        return data

    def grade(self, records, endpoint=GRADING_ENDPOINT):
        records = self.preprocess_records(records)
        return self.post(endpoint, data={RECORDS: records})


class CardConditionClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, resource_name="card-grader"):
        super().__init__(token=token, endpoint=endpoint, resource_name=resource_name)
        self.PREDICT_ENDPOINT = CONDITION_ENDPOINT

    def construct_data(self, records=[], mode=None):
        if len(records) == 0:
            raise Exception("Please specify at least one record in detect method!")
        data = {RECORDS: self.preprocess_records(records)}
        if mode:
            data["mode"] = mode
        return data

    def grade(self, records, mode=None, endpoint=CONDITION_ENDPOINT):
        return self.post(endpoint, data=self.construct_data(records, mode))


class CardCenteringClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, resource_name="card-grader"):
        super().__init__(token=token, endpoint=endpoint, resource_name=resource_name)
        self.PREDICT_ENDPOINT = CENTERING_ENDPOINT

    def construct_data(self, records=[], mode=None):
        if len(records) == 0:
            raise Exception("Please specify at least one record in detect method!")
        data = {RECORDS: self.preprocess_records(records)}
        return data

    def grade(self, records, mode=None, endpoint=CENTERING_ENDPOINT):
        return self.post(endpoint, data=self.construct_data(records, mode))


class CollectiblesRecognitionClient(RestClient):
    def __init__(self, token, endpoint=ENDPOINT, resource_name=COLLECTIBLES_RECOGNITION):
        super().__init__(token=token, endpoint=endpoint, resource_name=resource_name)
        self.PREDICT_ENDPOINT = COLLECTIBLES_ANALYZE

    def construct_data(self, records=[], lang=False, slab_id=False, slab_grade=False, fields_to_return=None, analyze_all=None, pricing=None):
        if len(records) == 0:
            raise Exception("Please specify at least one record in detect method!")
        data = {RECORDS: self.preprocess_records(records)}

        if lang:
            data["lang"] = lang

        if slab_id:
            data["slab_id"] = slab_id

        if fields_to_return:
            data["fields_to_return"] = fields_to_return

        if slab_grade:
            data["slab_grade"] = slab_grade

        if analyze_all:
            data["analyze_all"] = analyze_all

        if pricing:
            data["pricing"] = pricing

        return data

    def process(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_PROCESS, data=data)
        return result

    def card_id(
        self, records: list, lang: bool = False, slab_id: bool = False, slab_grade: bool = False, fields_to_return=None, analyze_all=None, pricing=None
    ):
        result = self.post(
            COLLECTIBLES_CARD_ID,
            data=self.construct_data(
                records, lang=lang, slab_id=slab_id, slab_grade=slab_grade, fields_to_return=fields_to_return, analyze_all=analyze_all, pricing=pricing
            ),
        )
        return result

    def tcg_id(self, records: list, lang: bool = False, slab_id: bool = False, slab_grade: bool = False, fields_to_return=None, analyze_all=None, pricing=None):
        # call card_id method with the same parameters
        return self.card_id(
            records, lang=lang, slab_id=slab_id, slab_grade=slab_grade, fields_to_return=fields_to_return, analyze_all=analyze_all, pricing=pricing
        )

    def sport_id(self, records: list, slab_id: bool = False, slab_grade: bool = False, fields_to_return=None):
        result = self.post(
            COLLECTIBLES_SPORT_ID,
            data=self.construct_data(
                records, slab_id=slab_id, slab_grade=slab_grade, fields_to_return=fields_to_return
            ),
        )
        return result

    def comics_id(self, records: list, slab_id: bool = False, slab_grade: bool = False, fields_to_return=None):
        result = self.post(
            COLLECTIBLES_COMICS_ID,
            data=self.construct_data(
                records, slab_id=slab_id, slab_grade=slab_grade, fields_to_return=fields_to_return
            ),
        )
        return result

    def detect(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_DETECT, data=data)
        return result

    def slab_id(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_SLAB_ID, data=data)
        return result

    def ocr_id(self, records: list):
        data = {RECORDS: self.preprocess_records(records)}
        result = self.post(COLLECTIBLES_OCR_ID, data=data)
        return result

    def analyze(self, records: list, fields_to_return=None):
        result = self.post(COLLECTIBLES_ANALYZE, data=self.construct_data(records, fields_to_return=fields_to_return))
        return result
