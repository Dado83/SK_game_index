import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_game_links(year):
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
        score = soup.select('.oc')[0].text.strip() if soup.select('.oc') else ''
        platform = ''
        if soup.find('tr', string='Platforma:'):
            platform = soup.find('tr', string='Platforma:').find_next('tr').text.strip()
        elif soup.find('tr', string='PLATFORMA:'):
            platform = soup.find('tr', string='PLATFORMA:').find_next('tr').text.strip()

        if platform == '' and soup.find('tr', string='Potrebno:'):
            platform = 'PC'

        if platform == '' and soup.find('tr', string='MINIMUM:'):
            platform = 'PC'
        date = soup.select('.autordatum')[1].text if soup.select('.autordatum') else ''
        date_temp = date.split(' ')
        date = date_temp[1] + ' ' + date_temp[2]
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
    return game_data


def merge_game_data(year, file_path):
    year = 1998
    merged_game_data = []

    while year <= 2020:
        f = open(file_path + str(year) + '.json', encoding='utf-8')
        file_content = f.read()
        merged_game_data += json.loads(file_content)
        f.close()
        year += 1

    return merged_game_data


def get_json_from_file(file_path):
    f = open(file_path, 'r')
    file_content = f.read()
    file_json = json.loads(file_content)
    f.close()
    return file_json


def save_json_to_file(file_path, data):
    f = open(file_path, 'ab')
    json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    f.write(json_data)
    f.close()
