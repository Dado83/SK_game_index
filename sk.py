import sk_test_play as sk

# fn used for updating game data
sk.scrape_all_game_data('e:/temp/', last_year=2020)

# fn used for writing data to single file
sk.save_json_to_file('e:/temp/sk.json', sk.merge_game_data('e:/temp/', 2020))
