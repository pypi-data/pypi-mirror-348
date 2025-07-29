from ximilar.client import RestClient
from ximilar.client.constants import *

FACE_DETECTION_ENDPOINT = "identity/v2/face"
PERSON_DETECTION_ENDPOINT = "identity/v2/person"


class XimilarIdentityClient(RestClient):
    def face(self, records):
        records = self.preprocess_records(records)
        return self.post(FACE_DETECTION_ENDPOINT, data={RECORDS: records})

    def person(self, records):
        records = self.preprocess_records(records)
        return self.post(PERSON_DETECTION_ENDPOINT, data={RECORDS: records})
