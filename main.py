import datetime
import sys
from collections import defaultdict, Counter

'''
    Function responsible for fetching the
    list of cars from defined API endpoint
'''
def fetch_page(
    date_from: int, 
    date_to: int, 
    page_number: int,
    number_of_elements_per_page: int
) -> dict:
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-XSRF-TOKEN': '1d7847a6-63ab-4651-bab3-ec75b4768698',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.copart.com',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    data = {
        'draw': '1',
        'columns[0][data]': '0',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': '1',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': '2',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'true',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': '3',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'true',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': '4',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'true',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': '5',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'true',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': '6',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'true',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': '7',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'true',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'columns[8][data]': '8',
        'columns[8][name]': '',
        'columns[8][searchable]': 'true',
        'columns[8][orderable]': 'true',
        'columns[8][search][value]': '',
        'columns[8][search][regex]': 'false',
        'columns[9][data]': '9',
        'columns[9][name]': '',
        'columns[9][searchable]': 'true',
        'columns[9][orderable]': 'true',
        'columns[9][search][value]': '',
        'columns[9][search][regex]': 'false',
        'columns[10][data]': '10',
        'columns[10][name]': '',
        'columns[10][searchable]': 'true',
        'columns[10][orderable]': 'true',
        'columns[10][search][value]': '',
        'columns[10][search][regex]': 'false',
        'columns[11][data]': '11',
        'columns[11][name]': '',
        'columns[11][searchable]': 'true',
        'columns[11][orderable]': 'true',
        'columns[11][search][value]': '',
        'columns[11][search][regex]': 'false',
        'columns[12][data]': '12',
        'columns[12][name]': '',
        'columns[12][searchable]': 'true',
        'columns[12][orderable]': 'true',
        'columns[12][search][value]': '',
        'columns[12][search][regex]': 'false',
        'columns[13][data]': '13',
        'columns[13][name]': '',
        'columns[13][searchable]': 'true',
        'columns[13][orderable]': 'true',
        'columns[13][search][value]': '',
        'columns[13][search][regex]': 'false',
        'columns[14][data]': '14',
        'columns[14][name]': '',
        'columns[14][searchable]': 'true',
        'columns[14][orderable]': 'false',
        'columns[14][search][value]': '',
        'columns[14][search][regex]': 'false',
        'columns[15][data]': '15',
        'columns[15][name]': '',
        'columns[15][searchable]': 'true',
        'columns[15][orderable]': 'false',
        'columns[15][search][value]': '',
        'columns[15][search][regex]': 'false',
        'order[0][column]': '1',
        'order[0][dir]': 'asc',
        'start': '0',
        'length': '20',
        'search[value]': '',
        'search[regex]': 'false',
        'sort': 'auction_date_type desc,auction_date_utc asc',
        'defaultSort': 'true',
        'filter[MISC]': 'go_app_user:*,#VehicleTypeCode:VEHTYPE_V,#LotYear:[2010 TO 2021]',
        'query': '*',
        'watchListOnly': 'false',
        'freeFormSearch': 'false',
        'page': str(page_number),
        'size': str(number_of_elements_per_page)
    }
    response = requests.post('https://www.copart.com/public/vehicleFinder/search', headers=headers, data=data)
    return response.json()
    
def list_all_records(
    date_from: int,
    date_to: int,
    number_of_elements_per_page: int,
    number_of_most_popular_makes_to_return: int
) -> list:
    '''
        Function responsible for 
        fetching all the records from website copart.com
        then counting each and every record
        finally returning tuples containing the most popular makes
    '''
    total_elements = 0
    page_number = 0
    dict_with_car_records = Counter()
    while(total_elements >= page_number * number_of_elements_per_page):
        website_json_response = fetch_page(
            date_from,
            date_to,
            page_number,
            number_of_elements_per_page
        )
        '''
            Replacing currently used number of total elements
            with one, that has been returned by the server
        '''
        total_elements = max(total_elements, website_json_response['data']['results']['totalElements'])
        '''
            Mapping make names, then counting these
        '''
        dict_with_car_records += Counter(map(lambda x: x['mkn'], website_json_response['data']['results']['content']))
        page_number += 1
    return dict_with_car_records.most_common(number_of_most_popular_makes_to_return)
print(str(list_all_records(2010, 2020, 20, 4)))