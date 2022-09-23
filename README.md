# leader_scraper 
leader_scraper is a Python snippet designed to download information about the main leaders from 5 countries. If you directly run it, it will output a json file containing a dictionary, with country as key ("be","fr","us","ma","ru") and a list of leaders dictionaries containing the main features of the leaders from wikipedia. 
## that's approximately the scheme:
{‘Nation1’:[{'id': 'leader1_id', 
'first_name': 'leader1_first_name', 
'last_name': 'leader1_last_name', 
'birth_date': 'leader1_birth_date', 
'death_date': 'leader1_death_date', 
'place_of_birth': 'leader1_place_of_birth', 
'wikipedia_url': 'leader1_wikipedia_url', 
'start_mandate': 'leader1_start_mandate’, 
'end_mandate': 'leader1_end_mandate',
'wikipedia_first_paragraph': 'leader1_wikipedia_first_paragraph'}, 
{leader2 ...}, 
...],
‘Nation2’: [leader1...]
...}

## This program was tested only on Python 3.10.4
To work properly it requires you to import te following: 
>- import json
>- import requests
>- import urllib3
>- from bs4 import BeautifulSoup
>- import re
and the and the corresponding dependencies
