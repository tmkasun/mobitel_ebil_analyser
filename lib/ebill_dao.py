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
        self._template = {
            '_id': None,
            Commons.MOBILE_NUMBER: {
                'owner': '',
                'type': 'Default',
                'bills': {
                }
            }
        }

    def add_ebill(self, ebill):
        call_data = ebill.data[Commons.CALL]
        mobile_no = ebill.data[Commons.MOBILE_NUMBER]
        bill_period = ebill.get_bill_period()

        if not self.get_ebills(mobile_no):
            mobile = self.add_new_mobile(mobile_no)
        else:
            mobile = self.get_ebills(mobile_no)
        update = {
            Commons.CALL: call_data
        }
        try:
            result = self._collection.update_one({'_id': mobile_no},
                                                 {'$set': {'{}.bills.{}.call'.format(mobile_no, bill_period): update}})
        except InvalidDocument as error:
            print(error)  # TODO: Do logging properly
        return result

    def get_ebills(self, mobile_number):
        return self._collection.find_one({'_id': mobile_number})

    def add_new_mobile(self, mobile_number):
        self._template['_id'] = mobile_number
        self._template[mobile_number] = self._template.pop(Commons.MOBILE_NUMBER)
        _id = self._collection.insert_one(self._template)
        return self.get_ebills(_id.inserted_id)
