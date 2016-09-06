import re


class Commons(object):
    CALL = "call"
    SMS = "sms"
    DATA = "data"
    BILL_CATEGORIES = [CALL, SMS, DATA]

    WITHIN_DATE_PATTERN = re.compile("(^\d*:\d*:\d*)\s*(\d*)\s*(\w)\s*(\d*)\s*(\d*?\.\d*)")
    BEGIN_DATE_PATTERN = re.compile(
            "(^[a-zA-Z]+\s+\d+\s+\d+)\s+(\d*:\d*:\d*)\s*(\d*)\s*(\w)\s*(\d*)\s*(\d*?\.\d*)")

    CALL_DATE_ENTRY_KEYS = ['TIME', 'NUMBER', 'STATUS', 'UNITS', 'COST']
    CALL_ENTRY_KEYS = ['DATE', 'TIME', 'NUMBER', 'STATUS', 'UNITS', 'COST']
