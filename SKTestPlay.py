import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_game_links():
    start_time = datetime.now().timestamp()
    first_year = 1998
    current_year = int(datetime.now().strftime('%Y'))
    base_url = 'https://www.sk.rs/arhiva/rubrika/test-play/'
    game_links = []
    time_elapsed = 0

    while first_year <= current_year:
        start_time_for_year_iteration = datetime.now().timestamp()
        test_play = requests.get(base_url + str(first_year))
        soup = BeautifulSoup(test_play.text, 'html.parser')
        links = soup.select('tr[valign=top] div.strana a.naslovmini')
        url = 'https://www.sk.rs/'

        for i in links:
            print(url + i.get('href'))
            game_links.append(url + i.get('href'))

        end_time_for_year_iteration = datetime.now().timestamp()
        time_to_complete_year_iteration = end_time_for_year_iteration - start_time_for_year_iteration
        time_minutes = int(time_to_complete_year_iteration / 60)
        time_seconds = round(time_to_complete_year_iteration % 60, 1)
        print(f'Time needed to get {first_year} links: {time_minutes}m {time_seconds}s')
        time_elapsed += time_to_complete_year_iteration
        elapsed_minutes = int(time_elapsed / 60)
        elapsed_seconds = round(time_elapsed % 60, 1)
        print(f'Time elapsed: {elapsed_minutes}m {elapsed_seconds}s')
        num_of_years_to_scrape = current_year - first_year
        approx_time_needed_to_get_all_links = time_to_complete_year_iteration * num_of_years_to_scrape
        approx_minutes = int(approx_time_needed_to_get_all_links / 60)
        approx_seconds = round(approx_time_needed_to_get_all_links % 60, 1)
        print(f'Time remaining: {approx_minutes}m {approx_seconds}s')
        first_year += 1

    end_time = datetime.now().timestamp()
    time_to_complete = end_time - start_time
    time_minutes = int(time_to_complete / 60)
    time_seconds = round(time_to_complete % 60, 1)
    print(f'Time needed to get all links: {time_minutes}m {time_seconds}s')
    return game_links


def scrape_game_data(links):
    start_time = datetime.now().timestamp()
    time_elapsed = 0
    game_list = []
    for link in links:
        start_time_link = datetime.now().timestamp()
        test_play = requests.get(link)
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
        time_to_finish = end_time_link - start_time_link
        time_minutes = int(time_to_finish / 60)
        time_seconds = round(time_to_finish % 60, 1)
        print(f'Time needed to scrape {link} data: {time_minutes}m {time_seconds}s')
        time_elapsed += time_to_finish
        elapsed_minutes = int(time_elapsed / 60)
        elapsed_seconds = round(time_elapsed % 60, 1)
        print(f'Time elapsed: {elapsed_minutes}m {elapsed_seconds}s')
        approx_time_needed_to_scrape_all_games = time_to_finish * len(links)
        approx_minutes = int(approx_time_needed_to_scrape_all_games / 60)
        approx_seconds = round(approx_time_needed_to_scrape_all_games % 60, 1)
        print(f'Time remaining: {approx_minutes}m {approx_seconds}s')

    end_time = datetime.now().timestamp()
    time_to_finish = end_time - start_time
    time_minutes = int(time_to_finish / 60)
    time_seconds = round(time_to_finish % 60, 1)
    print(f'Time needed to scrape data from all the games: {time_minutes}m {time_seconds}s')
    return game_list


'''
set utf-8
put data by year in separate files
fix total elapsed time needed for scraping counter
'''
