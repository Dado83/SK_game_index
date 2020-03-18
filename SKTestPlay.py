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
    file = open('e:/temp/links' + str(year) + '.txt', 'w')
    file_json = json.dumps(game_links)
    file.write(file_json)
    file.close()


def scrape_game_data(links):
    start_time = datetime.now().timestamp()
    time_elapsed = 0
    game_list = []
    for link in links:
        start_time_link = datetime.now().timestamp()
        test_play = requests.get(link)
        test_play.encoding = 'utf-8'
        soup = BeautifulSoup(test_play.text, 'html.parser')

        title = soup.select('.naslovstrana')[0].text if soup.select('.naslovstrana') else ''
        author = soup.select('.autordatum')[0].text if soup.select('.autordatum') else ''
        score = soup.select('.oc')[0].text if soup.select('.oc') else ''
        platform = ''
        if soup.find('tr', string='Platforma:'):
            platform = soup.find('tr', string='Platforma:').find_next('tr').text
        elif soup.find('tr', string='PLATFORMA:'):
            platform = soup.find('tr', string='PLATFORMA:').find_next('tr').text

        if platform == '' and soup.find('tr', string='Potrebno:'):
            platform = 'PC'

        if platform == '' and soup.find('tr', string='MINIMUM:'):
            platform = 'PC'
        date = soup.select('.autordatum')[1].text if soup.select('.autordatum') else ''
        link = test_play.url

        game_list.append({'title': title, 'author': author, 'score': score,
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
    return game_list


f = open('e:/temp/links1.txt', 'r')
file_content = f.read()
game_links = json.loads(file_content)
f.close()
game_data = scrape_game_data(game_links)
f = open('e:/temp/DATA.json', 'wb')
f.write(json.dumps(game_data, ensure_ascii=False).encode('utf-8'))
f.close()


'''
f = open('e:/temp/data.json', 'r')
data = f.read()
data_list = json.loads(data)

for d in data_list:
    print(d['date'])
'''
