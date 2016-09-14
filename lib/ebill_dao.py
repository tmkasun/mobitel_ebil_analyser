from pymongo import MongoClient
from bson.errors import InvalidDocument
from .commons import Commons
from .iebill_dao import IEbill_Dao

"""
client = MongoClient()
db = client.test
result = db.ebill.insert_one(
        {
            '_id': '0711661919',
            '0711661919': {
                'owner': 'Kasun Thennakoon',
                'type': 'Cpl sim',
                'bills': {
                    str(datetime.strptime('Jul 16', '%b %y').date()): {
                        'call': [],
                        'sms': [],
                        'data': []
                    }
                }
            }
        }
)

result
"""


class Ebill_Dao(IEbill_Dao):
    def __init__(self, db='knnect', collection='ebill'):
        self._client = MongoClient()
        self._collection = self._client[db][collection]

    def add_ebill(self, ebill):
        calls = ebill.get_call_records()
        results = None
        try:
            results = self._collection.insert_many(calls)
        except InvalidDocument as error:
            print(error)  # TODO: Do logging properly
        return results

    def get_ebills(self, mobile_number):
        return self._collection.find({'mobile_no': mobile_number})