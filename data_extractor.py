from bs4 import BeautifulSoup
from datetime import datetime
from lib.commons import Commons
from lib.ebill_dao import Ebill_Dao
import re


# http://beautiful-soup-4.readthedocs.io/en/latest/

class Ebill(object):
    def __init__(self, path):
        try:
            self._ebill_html = open(path, 'r')
        except FileNotFoundError:
            raise Exception("Given file {} path dose not exist\nPlease check the file path again.".format(path))
        self._ebill_soup = BeautifulSoup(self._ebill_html.read(), 'html.parser')
        self.pages = self._ebill_soup.find(id='page-container')
        self._init_vars()

    def _init_vars(self):
        # Initialize holding vars
        self.set_page_range(range(4, 6))
        self.data = dict(zip(Commons.BILL_CATEGORIES, [{} for _ in range(len(Commons.BILL_CATEGORIES))]))
        self._current_date = None

    def set_page_range(self, page_range):
        self.PAGE_RANGE = page_range

    def set_page_range(self, page_range):
        self.PAGE_RANGE = page_range

    def set_current_date(self, date):
        self._current_date = date

    def get_page_data(self, page_no):
        # start_call = data_page.contents[0].find(text=re.compile("Outgoing Call"))
        # page_data = {}  # date: entries
        data_page = self.pages.find(attrs={'data-page-no': page_no})
        if not data_page:
            return self.data
        siblings_generator = data_page.contents[0].contents[0].next_siblings
        # start_sms = data_page.contents[0].find(text=Commons.BEGIN_SMS_DATA_PATTERN)
        # if start_sms:
        #     siblings_generator = start_sms.parent.previous_siblings
        #     # TODO: Implement extracting SMS data
        #     # TODO: Handle SMS and DATA and other categories separately help: http://stackoverflow.com/questions/16835449/python-beautifulsoup-extract-text-between-element

        for data_element in siblings_generator:
            text_data = data_element.text.strip()
            if Commons.ACCOUNT_DETAILS_PATTERN.match(text_data): # TODO: Bad do use  different method
                matched_details = Commons.ACCOUNT_DETAILS_PATTERN.match(text_data).groups()
                self.update_account_details(matched_details)
            if Commons.BEGIN_SMS_DATA_PATTERN.match(text_data):
                break  # TODO: Bad do use  different method
            if Commons.WITHIN_DATE_PATTERN.match(text_data):
                data = Commons.WITHIN_DATE_PATTERN.match(text_data).groups()
                data = (self._current_date,) + data
                data_dict = dict(zip(Commons.CALL_ENTRY_KEYS, data))
                self.data[Commons.CALL][self._current_date.isoformat()].append(
                        data_dict)  # TODO: Check for _current_date before using
                # print("Match in date")
            elif Commons.BEGIN_DATE_PATTERN.match(text_data):
                data = Commons.BEGIN_DATE_PATTERN.match(text_data).groups()
                data_dict = dict(zip(Commons.CALL_ENTRY_KEYS, data))
                date = datetime.strptime(data_dict['DATE'], '%b %d %y')#.date()
                # date = date.isoformat() # TODO: replace this with good solution rather than converting to string
                # data_dict['DATE'] = date
                # TODO: Combine date and time together and add new key as TIMESTAP removing bothe DATE and TIME keys
                self.data[Commons.CALL][date.isoformat()] = [data_dict]
                self.set_current_date(date)
                # date_time_str = "{} {}".format(data_dict['DATE'], data_dict['TIME'])
                # date_time = datetime.strptime(date_time_str, '%b %d %y %H:%M:%S')

            else:
                pass
                # print(text_data)

    def set_total_payable(self):
        first_page = self.pages.find_all(class_='pf w0 h0')
        payable_pattern = re.compile("(Total Payable).*\s(\d*(\.\d.)?)")
        payable_string = first_page[0].contents[0].find_all(text=payable_pattern)
        self.data[Commons.TOTAL_AMOUNT] = re.match(payable_pattern, str(payable_string[0])).groups()[1]

    def set_bill_period(self):
        # TODO: Implement using Mobitel bill rotation dates i:e. Every month 20th day
        pass

    def get_bill_period(self):
        return 'bill-period'

    def update_account_details(self, matched_details):
        self.data[Commons.ACCOUNT_NUMBER] = matched_details[1]
        self.data[Commons.MOBILE_NUMBER] = matched_details[0]
        self.data

    def generate_bill(self):
        for page_no in self.PAGE_RANGE:
            self.get_page_data(page_no)
            print(len(self.data[Commons.CALL]))
        self.set_total_payable()
        self.set_bill_period()


def main():
    june_bill = Ebill('data/html/nh_ebill_preview_june.html')
    june_bill.generate_bill()
    ebill_dao = Ebill_Dao()
    ebill_dao.add_ebill(june_bill)


if __name__ == '__main__':
    main()
