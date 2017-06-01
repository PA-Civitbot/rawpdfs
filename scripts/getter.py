import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparse
from os.path import exists, join
from os import makedirs
import re
from slugify import slugify_url
from urllib.parse import urljoin


STASH_DIR = join('stash', 'fetched')
HOMEPAGE_URL = 'http://www.cityofpaloalto.org/gov/agendas/council/default.asp'
BASE_URL = 'http://www.cityofpaloalto.org/gov/agendas/council/'

MIN_YEAR = 2002
MAX_YEAR = 2017

def get_year_urls(year):
    things = []
    page_url = BASE_URL + str(year) + '.asp'
    resp = requests.get(page_url)
    soup = BeautifulSoup(resp.text, 'lxml')
    rows = soup.select('table tbody > tr')
    for row in rows:
        datetd = row.find('td')
        if datetd:
            rawdate = row.find('td').text
            if 'PIC' not in rawdate and re.search(r'\w+ +\d+ *, 20\d\d', rawdate):
                date = dateparse.parse(rawdate).strftime('%Y-%m-%d')
                for cell in row.select('td'):
                    link = cell.find('a')
                    if link and 'Video' not in link.text:
                        fname = date + '-' + slugify_url(link.text) + '.pdf'
                        url = urljoin(page_url, link['href'])
                        things.append((url, fname))
    return things


def download_and_save(url, filename):
    if not exists(filename):
        print("Downloading: " + url)
        resp = requests.get(url)
        with open(filename, 'wb') as f:
            print("Saving to:" + filename)
            f.write(resp.content)
    else:
        print('{} already exists'.format(filename))



if __name__ == '__main__':
    makedirs(STASH_DIR, exist_ok=True)
    years = list(range(MIN_YEAR, MAX_YEAR)) + ['default']
    for year in years:
        print(year)
        things = get_year_urls(year)
        for url, fname in things:
            fullname = join(STASH_DIR, fname)
            download_and_save(url, fullname)


