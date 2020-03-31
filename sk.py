import sk_test_play as sk

# update game data
sk.scrape_all_game_data('e:/temp/', last_year=2020)

# write data to single file
sk.save_json_to_file('e:/temp/sk.json', sk.merge_game_data('e:/temp/', 2020))

# create temp list consisting of only current year
list = sk.get_json_from_file('e:/temp/2020.json')
list.reverse()
sk.save_json_to_file('e:/temp/skTemp.json', list)
