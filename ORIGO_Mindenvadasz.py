# the following code is mainly based on an article:https://medium.com/analytics-vidhya/the-wayback-machine-scraper-63238f6abb66
# this code is using Wayback Server CDX API to Compile a list of URLs
# than in final_urls it constructs the main page of newssites that i scrape in order to get each hrefs that leads to the actual articles I need the texts from
# than I'm gonna get all the p elements from the list of hrefs that I got from the main pages in another code
# python packages for web scraping

import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep
from time import time
from warnings import warn
import json
import waybackpy
import time

start_time = time.time()

# Compile a list of URLs using Wayback Server CDX API(at
# https://web.archive.org/cdx/search/cdx) We  extract the desired urls
# into a json file to scrape tham later,

# Origo Wayback machine archive urls
urls = [
    'https://web.archive.org/cdx/search/cdx?url=https://www.origo.hu/itthon/index.html/&from=2011&to=2012&output=json'
    #     'https://web.archive.org/cdx/search/cdx?url=https://www.origo.hu/itthon/index.html/&from=2013&to=2014&output=json'
    #     'https://web.archive.org/cdx/search/cdx?url=https://www.origo.hu/itthon/index.html/&from=2016&to=2017&output=json'
    #     'https://web.archive.org/cdx/search/cdx?url=https://www.origo.hu/itthon/index.html/&from=2017&to=2018&output=json'
    #     'https://web.archive.org/cdx/search/cdx?url=https://www.origo.hu/itthon/index.html/&from=2018&to=2019&output=json'
    #     'https://web.archive.org/cdx/search/cdx?url=https://www.origo.hu/itthon/index.html/&from=2019&to=2020&output=json'
]

all_a_hrefs = set()  # empty set to store all the hrefs that we get in send request function

def get_final_urls():  # function to get the final urls from the json files that we extracted from the wayback machine
    parse_url = []
    for url in urls:
        response = rq.get(url)
        for d in json.loads(response.text):
            parse_url.append(d)

    # Extracts timestamp and original columns from urls and compiles a url
    url_list = []
    for i in range(1, len(parse_url)):
        orig_url = parse_url[i][2]
        tstamp = parse_url[i][1]
        waylink = tstamp + '/' + orig_url
        url_list.append(waylink)
    # Compiles final url pattern.
    final_urls = ['https://web.archive.org/web/' + url for url in url_list]
    print(f' final urls: {final_urls}')
    return final_urls


def send_request(index):
    try:
        if index == len(
                final_urls):  # if index is equal to the length of the list, then we have reached the end of the list
            return  # return nothing
        url = final_urls[index]

        response = rq.get(url)
        print(response.status_code)

        if response.status_code == 200:
            req = response.text
        # Parse the HTML using BeautifulSoup
            soup = bs(req, 'html.parser')
        # Find all href tags with the attribute
            a_hrefs = soup.find_all(
                'a', href=lambda href: href and 'www.origo.hu/nagyvilag' in href)
            for tag in a_hrefs:
                href = tag.get('href')
                if 'https://web.archive.org/web/' in href:
                    print(href)
                if href not in all_a_hrefs:
                    all_a_hrefs.add(href)
            time.sleep(7)
            send_request(index + 1)
        else:
            if response.status_code == 523:
                print(
                    f"Request to {url} failed with status code {response.status_code}")
                print('429 error: Im going to sleep for 2200 seconds')
                time.sleep(240)
                send_request(index)
            else:
                print(
                    f"Request to {url} failed with status code {response.status_code}")
                time.sleep(220)
                send_request(index)

    except BaseException:
        print('Something went wrong')
        time.sleep(220)
        send_request(index + 1)


def get_data(index2):
    try:
        # if index is equal to the length of the list, then we have reached the
        # end of the list
        if index2 == len(final_urls_element):
            return  # return nothing
        url = final_urls_element[index2]
        # Send GET request to the URL
        response = rq.get(url)
        if response.status_code == 200:
            req = response.text
            soup = bs(req, 'html.parser')
            p_tags = soup.find_all('p')
            p_texts = [p.get_text() for p in p_tags]
            datap = {'url': url, 'p_tags': p_texts}
            filename = url .replace(
                'https://',
                '').replace(
                'http://',
                '').replace(
                '/',
                '_').replace(
                '.',
                '_') + '.json'
            # Write data to a JSON file with a meaningful name based on the URL
            with open(filename, 'w', encoding='utf-8') as outfile:
                json.dump(datap, outfile, ensure_ascii=False)
                print(f'{filename} is ready!')
            time.sleep(8)
            get_data(index2 + 1)
        else:
            if response.status_code == 523:
                print(
                    f"Request to {url} failed with status code {response.status_code}")
                print('429 error: Im going to sleep for 2200 seconds')
                time.sleep(220)
                get_data(index2)

            else:
                print(
                    f"Request to {url} failed with status code {response.status_code}")
                time.sleep(22)
                get_data(index2)

    except BaseException:
        print('Something went wrong')
        time.sleep(420)
        get_data(index2)


final_urls = get_final_urls()
send_request(0)
final_urls_element = list(all_a_hrefs)
get_data(0)

print(final_urls_element)

end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time: {:.2f} seconds".format(elapsed_time))
print('Na most van kész')