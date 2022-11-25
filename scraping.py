import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

def getRawData(url):
    """
    url: link data from website www.estesparkweather.net

    e.g  https://www.estesparkweather.net/archive_reports.php?date=202211
    """
    # ======== Get HTML from url ============

    page = requests.get(url)
    soup =  BeautifulSoup(page.content,'html.parser')

    # =========================================
    # Data save tag table of html
    # get each row of table 
    # =========================================
    table = soup.find_all("table")
    raw_data = [row.text.splitlines() for row in table]
    raw_data = raw_data[:-9]

    for i in range(len(raw_data)):
        raw_data[i] = raw_data[i][2:len(raw_data[i]):3]

    return raw_data

if __name__ == "__main__":
    url= "https://www.estesparkweather.net/archive_reports.php?date=202211"
    raw_data = getRawData(url)
    print(raw_data[0])