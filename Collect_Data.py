import requests
import numpy as np

base_url = "https://old.chesstempo.com/requests/download_game_pgn.php?gameids="

url_offset = 4400000

num_grabs = 100

pgn_list=[]

while len(pgn_list)<num_grabs:
    print(url_offset)
    print(len(pgn_list))
    temp_url = base_url+str(url_offset)
    #split all the lines of the requested pgn
    parse = str(requests.get(temp_url).content).split("\\n")
    if len(parse) > 4:
        parse = parse[10]
        pgn_list.append(parse)
        url_offset+=1


for x in pgn_list:
    print(x)
    print()