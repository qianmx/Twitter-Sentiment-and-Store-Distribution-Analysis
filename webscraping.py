import urllib2
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd


def parseSN():
    response = urllib2.urlopen("http://www.nike.com/us/en_us/retail/en/directory")
    html = BeautifulSoup(response, "html.parser")
    states = defaultdict(list)
    for link in html.find_all('span', {'itemprop':'addressRegion'}):
        t = link.text
        t = t.replace('\n', '')
        if t in states:
            states[t] += 1
        else:
            states[t] = 1
    return states

if __name__ == '__main__':
    store_number = parseSN()
    df = pd.DataFrame(store_number.items(), columns=['States', 'StoreNumber'])
    df.to_csv('storenumber.csv')