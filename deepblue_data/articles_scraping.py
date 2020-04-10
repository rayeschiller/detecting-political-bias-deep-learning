import csv, pdb
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}

PARSE_FUNCTIONS = {
    'www.usatoday.com': lambda x: x.find_all('p', class_='gnt_ar_b_p')
}

DEFAULT_FUNC = lambda x: x.find_all('p')

def scraper():
    with open('deepblue_data/deepblue_labels.tsv') as csv_file:
            filereader = csv.DictReader(csv_file, delimiter='\t')
            count = 0
            for line in filereader:

                link = line['url']
                website = line['url'].split('/')[2]

                try:
                    content = requests.get(link, headers=HEADERS).content
                except:
                    print("Couldn't get article for %s" % link)
                    continue

                soup = BeautifulSoup(content)
                parse_func = PARSE_FUNCTIONS.get(website, DEFAULT_FUNC)

                paragraphs = [p.get_text() for p in parse_func(soup)]

                print('\n'.join(paragraphs))

                # NOTE: This break statement is temporarily put here to avoid running
                # this for thousands of articles. Modify as necessary.
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
    scraper()