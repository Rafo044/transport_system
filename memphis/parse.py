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
fetch_html(url)

def logging(message):
    timestamp_format = "%Y-%m-%d-%H-%M-%S"
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file , 'a') as f:
        f.write(timestamp + ',' + message +'\n')

def get_jobcontent(soup):
    # Tutaq ki, hər iş elanı <li class="vacancies__item"> elementindədir
    for li in soup.find_all("li", class_="vacancies__item"):
        a_tag = li.find("a", class_="vacancies__mobile-link")
        link = a_tag["href"] if a_tag else None 
        h2_tag = li.find("h2", class_="vacancies__title")
        title = h2_tag.get_text(strip=True) if h2_tag else None
        print(f"Processing title: {title}, link: {link}")

        # Əgər link varsa, onun detallı səhifəsini çəkək
        content_text = None
        if link:
            vacancy_soup = fetch_html(url + link)
            content_div = vacancy_soup.find("div", class_="vacancy__description content")
            content_text = content_div.get_text(separator="\n", strip=True) if content_div else None
            print(f"Fetched content for {title}: {content_text[:50]}...")  # İlk 50 simvolu çap edirik

        vacancies.append({"title": title, "link": link, "content": content_text})
        print(f"Title: {title}, Link: {link}, Content: {content_text[:50]}...")  # İlk 50 simvolu çap edirik

def job_list_csv(vacancies):
    df = pd.DataFrame(vacancies)  # dict siyahısından DataFrame yaratmaq
    df.to_csv(csv_file, index=False)

# İşin icrası

logging("Vacancy parsing started")

try:
    main_soup = fetch_html(url)
    logging("HTML web page successfully parsed")
except Exception as e:
    logging(f"Error fetching HTML: {str(e)}")
    print("Sorry. HTML Web page didn't respond.")
    exit()
print(fetch_html)
try:
    get_jobcontent(main_soup)
    logging("Job list parsed successfully")
except Exception as e:
    logging(f"Error parsing job list: {str(e)}")
    print("Sorry. Job list didn't parse.")
    exit()

try:
    job_list_csv(vacancies)
    logging("CSV file written successfully")
except Exception as e:
    logging(f"Error writing CSV: {str(e)}")
    print("Sorry. Couldn't write to CSV file.")
    exit()

logging("Vacancy parsing ended")
