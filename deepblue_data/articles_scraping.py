import csv, pdb
import requests
from bs4 import BeautifulSoup

def scraper():
    with open('deepblue_labels.tsv') as csv_file:
            filereader = csv.DictReader(csv_file, delimiter='\t')
            count = 0
            for line in filereader:

                link = line['url']

                try:
                    content = requests.get(link).content
                except:
                    print("Couldn't get article for %s" % link)
                    continue

                soup = BeautifulSoup(content)
                paragraphs = [p.get_text() for p in soup.find_all('p', class_='gnt_ar_b_p')]

                print('\n'.join(paragraphs))


def get_websites():
    websites = set() 
    with open('deepblue_labels.tsv') as csv_file:
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