import requests
import numpy as np
import logging
import http.client
import logging
import contextlib
from http.client import HTTPConnection # py3
import time
import random
import os
import sys

    
def parse_from_pgn():
    prints = False

    data_base = open(os.getcwd() + "\\DATABASE - Back Up.pgn","r",encoding="utf8",errors="ignore")
    fobj = open("PGN Only.txt","w",encoding="utf8",errors="ignore")
    pgn_list=[]
    # have to cap the final file size
    while len(pgn_list)<200000:
        line = data_base.readline()

        if line[0]!="[" and line!="\n":
            #wierd and bad pgn found, skip to next [
            if "{" in line or "$" in line:
                next_line = data_base.readline()
                while next_line[0]!="[":
                    next_line = data_base.readline()
            else:
                pgn = line
                line = data_base.readline()
                while line!="\n":
                    pgn+=" " + line
                    line = data_base.readline()
                    
                pgn = pgn.replace("\n", "")
                pgn = pgn+"\n"
                game_result = pgn[-4:-1]
                if len(pgn)<10:
                   if prints: print("pgn too short")
                elif "$" in pgn or "{" in pgn:
                   if prints: print("pgn contains $ or {")
                elif game_result !="1-0" and game_result!="0-1" and game_result !="1/2":
                   if prints: print("improper result format")
                elif pgn in pgn_list:
                    if prints: print("dupelicate game")
                else:
                    pgn_list.append(pgn)
                    fobj.write(pgn)
    
    data_base.close()
    fobj.close()
    
    
#parse_from_pgn()

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False
        
def download_tempo(num_grabs):
    base_url = "https://old.chesstempo.com/requests/download_game_pgn.php?gameids="
    session = requests.Session()
    url_offset = 0   
    fobj = open("test data.txt","w")
    
    pgn_list=[]
    failed_attempts=0

    
    while len(pgn_list)<num_grabs:
        
        url_offset = random.randint(4000000, 4900000)
    
        temp_url = base_url+str(url_offset)
        failed_attempts+=1
        
        #split all the lines of the requested pgn
        data = session.get(temp_url)
      
        parse = str(data.content).split("\n")
        if data.status_code!=200:
            print(data.status_code)
            pass
        elif parse == "b''": pass
    
        for s in parse:
            if len(s)>20 and s[0] == "1":
                failed_attempts-=1
                pgn_list.append(s)
                fobj.write(s)
                fobj.write("\n")
                break
    fobj.close()

