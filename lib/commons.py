import re


class Commons(object):
    CALL = "call"
    SMS = "sms"
    DATA = "data"
    ACCOUNT_NUMBER = 'account_no'
    MOBILE_NUMBER = 'mobile_no'
    TOTAL_AMOUNT = 'total'
    BILL_CATEGORIES = [CALL, SMS, DATA]
    # Pre compiled patterns for recognizing different categories
    WITHIN_DATE_PATTERN = re.compile("(^\d*:\d*:\d*)\s*(\d*)\s*(\w)\s*(\d*)\s*(\d*?\.\d*)")
    BEGIN_DATE_PATTERN = re.compile(
            "(^[a-zA-Z]+\s+\d+\s+\d+)\s+(\d*:\d*:\d*)\s*(\d*)\s*(\w)\s*(\d*)\s*(\d*?\.\d*)")
    BEGIN_SMS_DATA_PATTERN = re.compile("SMS Outgoing")
    ACCOUNT_DETAILS_PATTERN = re.compile("Call Charge Details for Mobile No : (\d+) of Account (\d+)")

    CALL_ENTRY_KEYS = ['date', 'time', 'number', 'status', 'units', 'cost']
