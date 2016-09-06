from bs4 import BeautifulSoup
from datetime import datetime
from lib.commons import Commons
import re


# http://beautiful-soup-4.readthedocs.io/en/latest/

class Ebill(object):

    def __init__(self, path):
        try:
            self._ebill_html = open(path, 'r')
        except FileNotFoundError as fnf:
            raise Exception("Given file {} path dose not exist\nPlease check the file path again.".format(path))
        self._ebill_soup = BeautifulSoup(self._ebill_html.read(), 'html.parser')
        self.pages = self._ebill_soup.find(id='page-container')
        self._init_vars()

    def _init_vars(self):
        # Initialize holding vars
        self.PAGE_RANGE = range(5, 6)
        self.ebill_data = dict(zip(Commons.BILL_CATEGORIES, [None for _ in range(len(Commons.BILL_CATEGORIES))]))
        self._current_date = None

    def set_page_range(self, page_range):
        self.PAGE_RANGE = page_range

    def set_current_date(self, date):
        if not type(date) is datetime:
            raise Exception("Invalid date format")
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

        for data_element in data_page.contents[0].contents[0].next_siblings:
            text_data = data_element.text.strip()
            # print(text_data)
            if Commons.WITHIN_DATE_PATTERN.match(text_data):
                data = Commons.WITHIN_DATE_PATTERN.match(text_data).groups()
                data_dict = dict(zip(Commons.CALL_DATE_ENTRY_KEYS, data))
                self.ebill_data[self._current_date].append(data_dict)
                # print("Match in date")
            elif Commons.BEGIN_DATE_PATTERN.match(text_data):
                data = Commons.BEGIN_DATE_PATTERN.match(text_data).groups()
                data_dict = dict(zip(Commons.CALL_ENTRY_KEYS, data))
                date = datetime.strptime(data_dict['DATE'], '%b %d %y').date()
                self.ebill_data[date] = [data_dict]
                self.set_current_date(date)
                # date_time_str = "{} {}".format(data_dict['DATE'], data_dict['TIME'])
                # date_time = datetime.strptime(date_time_str, '%b %d %y %H:%M:%S')

            else:
                pass
                # print(text_data)

        return page_data

    def getTotalPayable(self):
        first_page = self.pages.find_all(class_='pf w0 h0')
        payable_pattern = re.compile("(Total Payable).*\s(\d*(\.\d.)?)")
        payable_string = first_page[0].contents[0].find_all(text=payable_pattern)
        return re.match(payable_pattern, str(payable_string[0])).groups()[1]


a = Ebill('data/ebill_preview.htmla')
assert False


def main():
    bill_info = {}
    ebill_html = open('data/ebill_preview.html', 'r')
    ebill_soup = BeautifulSoup(ebill_html.read(), 'html.parser')
    pages = ebill_soup.find(id='page-container')
    bill_info['TOTP'] = getTotalPayable(pages)
    STARTING_PAGE = 4
    END_PAGE = 6
    pages_data = {}
    # TODO: Handle SMS and DATA and other categories separately help: http://stackoverflow.com/questions/16835449/python-beautifulsoup-extract-text-between-element
    for page in range(STARTING_PAGE, END_PAGE):
        pages_data = get_page_data(pages, page, pages_data)
        print(len(pages_data))

    pages_data


current_date = None
found_sms_section = False

if __name__ == '__main__':
    main()
