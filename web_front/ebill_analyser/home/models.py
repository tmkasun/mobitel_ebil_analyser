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
        details = []
        current = next(frequencies, None)
        while current:
            details.append(current)
            current = next(frequencies, None)
        return details
