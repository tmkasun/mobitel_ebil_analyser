from bs4 import BeautifulSoup
from datetime import datetime
import re


# http://beautiful-soup-4.readthedocs.io/en/latest/

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

def get_page_data(pages, page_no, page_data=None):
    # start_call = data_page.contents[0].find(text=re.compile("Outgoing Call"))
    # page_data = {}  # date: entries

    if page_data is None:
        page_data = {}
    global current_date, found_sms_section  # TODO: this looks ugly change whole thing in to Object O
    data_page = pages.find(attrs={'data-page-no': page_no})
    if not data_page:
        return page_data
    start_sms = data_page.contents[0].find(text=re.compile("SMS Outgoing"))
    if start_sms:
        found_sms_section = True
        # TODO: Implement extracting SMS data
    in_date_pattern = re.compile("(^\d*:\d*:\d*)\s*(\d*)\s*(\w)\s*(\d*)\s*(\d*?\.\d*)")
    begin_date_pattern = re.compile("(^[a-zA-Z]+\s+\d+\s+\d+)\s+(\d*:\d*:\d*)\s*(\d*)\s*(\w)\s*(\d*)\s*(\d*?\.\d*)")
    for data_element in data_page.contents[0].contents[0].next_siblings:
        text_data = data_element.text.strip()
        # print(text_data)
        if in_date_pattern.match(text_data):
            data = in_date_pattern.match(text_data).groups()
            keys = ['TIME', 'NUMBER', 'STATUS', 'UNITS', 'COST']
            data_dict = dict(zip(keys, data))
            page_data[current_date].append(data_dict)
            # print("Match in date")
        elif begin_date_pattern.match(text_data):
            data = begin_date_pattern.match(text_data).groups()
            keys = ['DATE', 'TIME', 'NUMBER', 'STATUS', 'UNITS', 'COST']
            data_dict = dict(zip(keys, data))
            date = datetime.strptime(data_dict['DATE'], '%b %d %y').date()
            page_data[date] = [data_dict]
            current_date = date
            # date_time_str = "{} {}".format(data_dict['DATE'], data_dict['TIME'])
            # date_time = datetime.strptime(date_time_str, '%b %d %y %H:%M:%S')

        else:
            pass
            # print(text_data)

    return page_data


def getTotalPayable(pages):
    first_page = pages.find_all(class_='pf w0 h0')
    payable_pattern = re.compile("(Total Payable).*\s(\d*(\.\d.)?)")
    payable_string = first_page[0].contents[0].find_all(text=payable_pattern)
    return re.match(payable_pattern, str(payable_string[0])).groups()[1]


if __name__ == '__main__':
    main()
