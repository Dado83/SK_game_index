import sk_test_play as sk


sk.save_json_to_file('e:/temp/data.json', sk.scrape_game_data(sk.get_json_from_file('e:/temp/links2020.txt')))
