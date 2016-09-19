from django.db import models
from mongoengine import StringField, Document


# Create your models here.

class Ebill(Document):
    number = StringField()
    mobile_no = StringField()
    timestamp = StringField()
    account_no = StringField()
    units = StringField()
    status = StringField()
    cost = StringField()

    @staticmethod
    def get_call_frequencies():
        frequencies = Ebill.objects.aggregate({'$group': {'_id': "$number", 'count': {'$sum': 1}}},
                                              {'$sort': {"count": -1}})
        return Ebill._cursor_to_list(frequencies)

    @staticmethod
    def get_calls_per_day():
        calls_per_day = Ebill.objects.aggregate(
                {'$project': {'ymd': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$timestamp"}}}},
                {'$group': {'_id': "$ymd", 'count': {'$sum': 1}}},
                {'$sort': {"_id": -1}})
        return Ebill._cursor_to_list(calls_per_day)

    @staticmethod
    def _cursor_to_list(cursor):
        details = []
        current = next(cursor, None)
        while current:
            details.append(current)
            current = next(cursor, None)
        return details
