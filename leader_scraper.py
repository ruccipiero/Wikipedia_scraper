import json
import requests
import urllib3
from bs4 import BeautifulSoup
import re

#to speed up things i decided to work with session
session = requests.Session()
#get the first paragraph
    #to speed up things i decided to set up caches
cache = {}
def hashable_cache(f):
    def inner(url, session):
        if url not in cache:
            cache[url] = f(url, session)
        return cache[url]
    return inner
    #to get the first paragraph
@hashable_cache
def get_first_paragraph(wikipedia_url, session):
    wikipedia_page = session.get(wikipedia_url).text
    soup = BeautifulSoup(wikipedia_page, 'html.parser')
    paragraphs = [tag for tag in soup.find_all("p")]
    for paragraph in paragraphs:
        if paragraph.find('b'):
            infected_first_paragraph = paragraph.get_text()
            break
    regex = r'\[.\]|\(.+\)|\\n'
    first_paragraph = re.sub(regex,"",infected_first_paragraph,flags=re.IGNORECASE)
    return first_paragraph 
# to get the leaders info, I've set up a specific function
def get_leaders():
    """ get_leaders creates a dictionary with countires and leaders from wikipedia for some countries. 
    it requires to import the "requests" library to work. """
    root_url = 'https://country-leaders.herokuapp.com'
    cookie_url = root_url+"/cookie"
    session = requests.Session()
    req = session.get(cookie_url)
    cookies = req.cookies
    country_url = root_url+'/countries'
    countries = session.get(country_url, cookies=cookies)
    leaders_per_country = {}
    json_countries = countries.json()
    leaders_url = root_url+"/leaders"
    for country in json_countries:
        params = {"country":country}
        req_country_leaders = session.get(leaders_url, cookies=cookies, params=params)
        if req_country_leaders.status_code == 403:
            req = requests.get(cookie_url)
            cookies = req.cookies
            countries = requests.get(country_url, cookies=cookies)
            json_countries = countries.json()
            params = {"country":country}
            req_country_leaders = requests.get(leaders_url, cookies=cookies, params=params)
        else:
            pass
        country_leaders = req_country_leaders.json()
        for country_leader in country_leaders:
            country_leader['first_paragraph'] = get_first_paragraph(country_leader['wikipedia_url'],session)
        leaders_per_country[country] = country_leaders
    return leaders_per_country
#save the file
leaders_per_country = get_leaders()
def save(leaders_per_country):
    with open('./leaders.json',"w") as leaders:
        json.dump(leaders_per_country, leaders)
save(leaders_per_country)
print("\"leaders.json\" file downloaded")
