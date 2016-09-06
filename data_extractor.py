from bs4 import BeautifulSoup
from datetime import datetime
from lib.commons import Commons
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
        self.ebill_data = dict(zip(Commons.BILL_CATEGORIES, [{} for _ in range(len(Commons.BILL_CATEGORIES))]))
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
            return self.ebill_data
        start_sms = data_page.contents[0].find(text=re.compile("SMS Outgoing"))
        if start_sms:
            self.ebill_data[Commons.SMS] = True
            # TODO: Implement extracting SMS data
            # TODO: Handle SMS and DATA and other categories separately help: http://stackoverflow.com/questions/16835449/python-beautifulsoup-extract-text-between-element

        for data_element in data_page.contents[0].contents[0].next_siblings:
            text_data = data_element.text.strip()
            print(text_data)
            if Commons.WITHIN_DATE_PATTERN.match(text_data):
                data = Commons.WITHIN_DATE_PATTERN.match(text_data).groups()
                data_dict = dict(zip(Commons.CALL_DATE_ENTRY_KEYS, data))
                self.ebill_data[Commons.CALL][self._current_date].append(data_dict) # Check for _current_date
                # print("Match in date")
            elif Commons.BEGIN_DATE_PATTERN.match(text_data):
                data = Commons.BEGIN_DATE_PATTERN.match(text_data).groups()
                data_dict = dict(zip(Commons.CALL_ENTRY_KEYS, data))
                date = datetime.strptime(data_dict['DATE'], '%b %d %y').date()
                self.ebill_data[Commons.CALL][date] = [data_dict]
                self.set_current_date(date)
                # date_time_str = "{} {}".format(data_dict['DATE'], data_dict['TIME'])
                # date_time = datetime.strptime(date_time_str, '%b %d %y %H:%M:%S')

            else:
                pass
                # print(text_data)

    def get_total_payable(self):
        first_page = self.pages.find_all(class_='pf w0 h0')
        payable_pattern = re.compile("(Total Payable).*\s(\d*(\.\d.)?)")
        payable_string = first_page[0].contents[0].find_all(text=payable_pattern)
        self.ebill_data['TOTAL'] = re.match(payable_pattern, str(payable_string[0])).groups()[1]

    def generate_bill(self):
        for page_no in self.PAGE_RANGE:
            self.get_page_data(page_no)
            print(len(self.ebill_data))
        self.get_total_payable()


def main():
    aug_bill = Ebill('data/ebill_preview.html')
    aug_bill.generate_bill()
    aug_bill
if __name__ == '__main__':
    main()
