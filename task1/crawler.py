# -*- coding:utf-8 -*-

import urllib
import json
import logging
import sys

from bs4 import BeautifulSoup
import Levenshtein
from tqdm import tqdm


def get_google_results(url):
    try:
        with urllib.request.urlopen(url) as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find(id='rcnt')
        groups = content.findAll('div', {'class': 'g'})
        infos = list()
        for idx, group in enumerate(groups):
            a = group.find('h3').find('a')
            title = a.get_text()
            url = a['href']
            abstract = group.find('span', {'class': 'st'}).get_text()
            infos.append({'title': title, 'url': url, 'abstract': abstract, 'index': idx})
    except:
        logger.error(url)
    return infos

def get_all_urls(url):
    urls = list()
    try:
        with urllib.request.urlopen(url, timeout=2) as f:
            html = f.read()
    except urllib.error.URLError as err:
        logging.error(err)
        return urls
    except Exception as err:
        logging.exception(err)
        return urls
    soup = BeautifulSoup(html, 'html.parser')
    a_list = soup.findAll('a')
    for a in a_list:
        url = a.get('href')
        if url and url.startswith('http'):
            urls.append((a.get_text(), url))
    return urls


def query_google_results(query_strings, url):
    infos = get_google_results(url)
    total = list()
    for info in infos:
        url = info['url']
        try:
            with urllib.request.urlopen(url, timeout=2) as f:
                html = f.read()
                info['reachable'] = 1
        except urllib.error.URLError as err:
            logging.error(err)
            info['reachable'] = 0
        except Exception as err:
            logging.exception(err)
            info['reachable'] = 0
        src = query_strings
        title = info['title']
        abstract = info['abstract']
        info['title_edit_dist'] = Levenshtein.distance(src, title)
        info['title_ratio'] = Levenshtein.ratio(src, title)
        info['abstract_edit_dist'] = Levenshtein.distance(src, abstract)
        info['abstract_ratio'] = Levenshtein.ratio(src, abstract)
    return infos

def main():
    with open(sys.argv[1]) as fp:
        infos = list()
        tmp = {}
        for idx, line in enumerate(tqdm(fp, total=66000)):
            if (idx + 1) % 11 == 0:
                infos.append(tmp)
                query_strings = tmp['#name'] + ' ' + tmp['#org']
                query_url = tmp['#search_results_page']
                results = query_google_results(query_strings, query_url)
                print(json.dumps(results, indent=2))
                tmp = {}
            else:
                key, value = line.strip().split(':', 1)
                tmp[key] = value

if __name__ == '__main__':
#    infos = get_google_results('http://ifang.ml:8081/53f45c1ddabfaee2a1d891a1.html')
#    total = list()
#    for info in infos:
#        url = info['url']
#        total.append(url)
#        logging.error('get url %s' %(url))
#        tmp = get_all_urls(url)
#        total.extend(tmp)
#    for info in tmp:
#        logging.error('scan secondary urls')
#        url = info[1]
#        logging.error('get url %s' %(url))
#        total.extend(get_all_urls(url))
#    print(json.dumps(total, indent=2))
    main()
