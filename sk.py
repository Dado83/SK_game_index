import sk_test_play as sk


# update game data
sk.scrape_all_game_data('e:/temp/sk/', year=2021)

# write data to single file
sk.save_json_to_file('e:/temp/sk.json', sk.merge_game_data('e:/temp/sk/', 2021))

# create temp list consisting of only current year
list = sk.get_json_from_file('e:/temp/sk/2021.json')
list.reverse()
sk.save_json_to_file('e:/temp/skTemp.json', list)


""" 
# test code for individual link
link = ['https://www.sk.rs//arhiva/clanak/28030/detroit-become-human-pc']
data = sk.scrape_game_data(link)
for d in data:
    print(d)
 """
