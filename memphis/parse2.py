from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

url = "https://classic.jobsearch.az/vacancies/"
log_file = "log_file.txt"
csv_file = "vacancies.csv"
vacancies = []

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()  # səhv olsa exception atacaq
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup
print(fetch_html(url))