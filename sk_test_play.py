import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_game_links(year):
    '''Get game links by year'''

    base_url = 'https://www.sk.rs/arhiva/rubrika/test-play/'
    time_elapsed = 0
    start_time_for_year_iteration = datetime.now().timestamp()
    test_play = requests.get(base_url + str(year))
    soup = BeautifulSoup(test_play.text, 'html.parser')
    links = soup.select('tr[valign=top] div.strana a.naslovmini')
    url = 'https://www.sk.rs/'
    game_links = []

    for i in links:
        print(url + i.get('href'))
        game_links.append(url + i.get('href'))

    end_time_for_year_iteration = datetime.now().timestamp()
    time_to_complete_year_iteration = end_time_for_year_iteration - start_time_for_year_iteration
    time_minutes = int(time_to_complete_year_iteration / 60)
    time_seconds = round(time_to_complete_year_iteration % 60, 1)
    print(f'Time needed to get {year} links: {time_minutes}m {time_seconds}s')
    time_elapsed += time_to_complete_year_iteration
    elapsed_minutes = int(time_elapsed / 60)
    elapsed_seconds = round(time_elapsed % 60, 1)
    print(f'Time elapsed: {elapsed_minutes}m {elapsed_seconds}s')
    return game_links


def scrape_game_data(links):
    '''Scrape game data from link'''

    start_time = datetime.now().timestamp()
    time_elapsed = 0
    game_data = []
    for link in links:
        start_time_link = datetime.now().timestamp()
        test_play = requests.get(link)
        test_play.encoding = 'utf-8'
        soup = BeautifulSoup(test_play.text, 'html.parser')

        title = soup.select('.naslovstrana')[0].text.strip() if soup.select('.naslovstrana') else ''
        author = soup.select('.autordatum')[0].text.strip() if soup.select('.autordatum') else ''
        score = soup.select('.oc')[0].text.strip() if soup.select('.oc') else soup.select(
            '.Arhiva-Ocena')[0].text.strip() if soup.select('.Arhiva-Ocena') else ''
        platform = ''
        if soup.find('tr', string='Platforma:'):
            platform = soup.find('tr', string='Platforma:').find_next('tr').text.strip()
        elif soup.find('tr', string='PLATFORMA:'):
            platform = soup.find('tr', string='PLATFORMA:').find_next('tr').text.strip()
        elif soup.find('tr', string='Platfoma:'):
            platform = soup.find('tr', string='Platfoma:').find_next('tr').text.strip()
        elif soup.select('.Arhiva-Kategorija'):
            for el in soup.select('.Arhiva-Kategorija'):
                if 'Platforma' in el.text:
                    platform = el.text.strip('Platforma:').strip()

        if platform == '' and (soup.find('tr', string='Potrebno:')
                               or soup.find('tr', string='POTREBNO:')
                               or soup.find('tr', string='MINIMUM:')
                               or soup.find('tr', string='Minimum:')
                               or soup.find('tr', string='Putrebno:')
                               or soup.find('tr', string='aPotrebno:')
                               or soup.find('tr', string='Veličina:')
                               ):
            platform = 'PC'

        date = soup.select('.autordatum')[1].text if soup.select('.autordatum') else ''
        date_temp = date.split(' ')
        date_month = format_date(date_temp[1])
        date = str(date_month) + '.' + date_temp[2]
        link = test_play.url

        game_data.append({'title': title, 'author': author, 'score': score,
                          'platform': platform, 'date': date, 'link': link})

        end_time_link = datetime.now().timestamp()
        time_to_finish_link_scrape = end_time_link - start_time_link
        time_minutes = int(time_to_finish_link_scrape / 60)
        time_seconds = round(time_to_finish_link_scrape % 60, 1)
        print(f'Time needed to scrape {link} data: {time_minutes}m {time_seconds}s')
        time_elapsed += time_to_finish_link_scrape
        elapsed_minutes = int(time_elapsed / 60)
        elapsed_seconds = round(time_elapsed % 60, 1)
        print(f'Time elapsed: {elapsed_minutes}m {elapsed_seconds}s')

    end_time = datetime.now().timestamp()
    time_to_finish = end_time - start_time
    total_minutes = int(time_to_finish / 60)
    total_seconds = round(time_to_finish % 60, 1)
    print(f'Time needed to scrape all data: {total_minutes}m {total_seconds}s')
    game_data.reverse()
    return game_data


def format_date(date):
    '''Helper fn for month format'''

    months = {'januar': '01', 'februar': '02', 'mart': '03', 'april': '04', 'maj': '05', 'jun': '06',
              'jul': '07', 'avgust': '08', 'septembar': '09', 'oktobar': '10', 'novembar': '11', 'decembar': '12'}
    for m in months:
        if date == m:
            return months[m]


def merge_game_data(file_path, last_year):
    '''Takes separate json files and merges them in a single json file'''

    year = 1998
    merged_game_data = []

    while year <= last_year:
        with open(file_path + str(year) + '.json', encoding='utf-8') as f:
            file_content = f.read()
        merged_game_data += json.loads(file_content)
        year += 1
    merged_game_data.reverse()
    return merged_game_data


def get_json_from_file(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()
    file_json = json.loads(file_content)
    return file_json


def save_json_to_file(file_path, data):
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    with open(file_path, 'wb') as f:
        f.write(json_data)
    return True


def scrape_all_game_data(path, year=None, last_year=None):
    '''Scrapes game data by year and saves it in separate json files'''

    start_time = datetime.now().timestamp()
    if last_year:
        start_year = 1998
        while start_year <= last_year:
            save_json_to_file(path + str(start_year) + '.json', scrape_game_data(get_game_links(start_year)))
            start_year += 1
    else:
        save_json_to_file(path + str(year) + '.json', scrape_game_data(get_game_links(year)))

    end_time = datetime.now().timestamp()
    time_to_finish = end_time - start_time
    total_minutes = int(time_to_finish / 60)
    total_seconds = round(time_to_finish % 60, 1)
    print(f'Time needed to scrape TEST PLAY: {total_minutes}m {total_seconds}s')
