import csv, pdb, json
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

PARSE_FUNCTIONS = {
    'www.usatoday.com': lambda x: x.find_all('p', class_='gnt_ar_b_p'),
    'latimesblogs.latimes.com': lambda x: x.find_all('p'),
    'jp.wsj.com': lambda x: x.find_all('p'),
    'india.blogs.nytimes.com': lambda x: x.find_all('p', class="story-body-text"),
    'ph.news.yahoo.com': lambda x: x.find_all('p'),
    'buzz.money.cnn.com': lambda x: x.find_all('p'),
    'krugman.blogs.nytimes.com': lambda x: x.find_all('p', class="story-body-text"),
    'www.nbcnews.com': lambda x: x.find_all('p'),
    'www.foxnews.com': lambda x: x.find_all('p'),
    'www.nytimes.com': lambda x: x.find_all ('p', class="css-exrw3m evys1bk0"),
    'www.latimes.com': lambda x: x.find_all('p'),
    'uk.news.yahoo.com': lambda x: x.find_all ('p', class="canvas-atom canvas-text Mb(1.0em) Mb(0)--sm Mt(0.8em)--sm"),
    "takingnote.blogs.nytimes.com": lambda x: x.find_all ('p', class="story-body-text"),
    'www.latimes.comthelead.blogs.cnn.com': lambda x: x.find_all('p'),
    'ftw.usatoday.com': lambda x: x.find_all('p'),
    'presspass.nbcnews.com': lambda x: x.find_all('p'),
    'blogs.chicagotribune.com': lambda x: x.find_all('p'),    
    'us.cnn.com': lambda x: x.find_all('div', class_='zn-body__paragraph')
}

DEFAULT_FUNC = lambda x: x.find_all('p')

def read_from_tsv():
    with open('deepblue_data/deepblue_labels.tsv') as csv_file:
            filereader = csv.DictReader(csv_file, delimiter='\t')
            for line in filereader:
                yield line

def scraper(read_func):
    output = []
    count = 1

    with open('scraped_data_all.tsv', 'w') as csvfile:
        fields = ['url', 'q3', 'perceived', 'primary.topic', 'secondary.topic',	'democrat.vote', 'republican.vote', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter='\t')
        writer.writeheader()

        for row in read_func():
            print("Getting link no: %d" % count)
            link = row['url']
            website = link.split('/')[2]

            try:
                content = requests.get(link, headers=HEADERS).content
            except:
                try:
                    content = requests.get(link).content
                except:
                    print("Couldn't get article for %s" % link)
                    continue

            soup = BeautifulSoup(content)
            parse_func = PARSE_FUNCTIONS.get(website, DEFAULT_FUNC)

            paragraphs = [p.get_text() for p in parse_func(soup)]

            row.update({'content': '\n'.join(paragraphs)})
            writer.writerow(row)
            count += 1

            # NOTE: This break statement is temporarily put here to avoid running
            # this for thousands of articles. Modify as necessary.
            if count > 5:
                break

def get_websites():
    websites = set() 
    with open('deepblue_data/deepblue_labels.tsv') as csv_file:
        filereader = csv.DictReader(csv_file, delimiter='\t')

        for line in filereader:
            if 'url' not in line:
                print(line)
                continue

            splits = line['url'].split('/')

            if len(splits) > 2:
                websites.add(splits[2])
            else:
                websites.add(line['url'])
    return websites


if __name__ == "__main__":
    scraper(read_from_tsv)