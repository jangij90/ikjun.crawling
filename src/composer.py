# encoding: utf-8


'''
author: Ikjun Jang
email: jangij90@gmail.com
function : 작곡가 가져오기, 작곡가 다른 이름 가져오기
'''


import os
import re
import requests
import time

from bs4 import BeautifulSoup


# 다음 페이지 가져오기
def get_next_categorypaginglink(html):
    time.sleep(1)
    categorypaginglink = None
    page_links = html.find_all('a', href=True, class_='categorypaginglink')
    for page_link in page_links:
        if 'next' in page_link.text:
            categorypaginglink = page_link['href']
            break
    return categorypaginglink


# 작곡가 명 가져오기
def get_name_from_yyy(baselink=None):

    baseurl = 'http://imslp.org'
    categorylink = None
    if baselink:
        title = None
        data = None

        resp = requests.get(baseurl + baselink)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            categorylink = get_next_categorypaginglink(soup)

            for v in soup.find_all('a', href=True, class_='categorysubcatlink'):
                if v.get_text(strip=True):
                    link = v['href']
                    title = v['title'].split(':')
                    title = title[1]
                    data = str(title) + '^' + str(link) + os.linesep
                    data = bytes(data.encode('utf-8'))

                    with open(path, 'ab+') as file:
                        file.write(data)

            if categorylink:
                get_name_from_yyy(categorylink)
            else:
                return None
    else:
        title = None
        data = None
        crawlingURL = '/wiki/Category:Composers'

        resp = requests.get(baseurl + crawlingURL)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            categorylink = get_next_categorypaginglink(soup)

            for v in soup.find_all('a', href=True, class_='categorysubcatlink'):
                if v.get_text(strip=True):
                    link = v['href']
                    title = v['title'].split(':')
                    title = title[1]
                    data = str(title) + '^' + str(link) + os.linesep
                    # data = ''.join([str(title), ':', str(link), os.linesep])
                    data = bytes(data.encode('utf-8'))

                    with open(path, 'ab+') as file:
                        file.write(data)

            if categorylink:
                get_name_from_yyy(categorylink)
            else:
                return None

    return None


# 작곡가 다른 언어명 and 별칭 가져오기
def get_nick_from_name(basecomposer=None, baselink=None):

    baseurl = 'http://imslp.org'
    data = {}
    nick = {}
    trans = {}
    n_flag = False
    t_flag = False
    # baselink = '/wiki/Category:Aagesen,_Truid'
    # baselink = '/wiki/Category:Beethoven,_Ludwig_van'
    resp = requests.get(baseurl + baselink)
    
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        test = soup.find_all('div', class_='plainlinks cp_mainlinks')
        data['composer'] = basecomposer
        if test:
            for v in test[0].find_all('span'):
                if v.get_text(strip=True):
                    if v.text.find('Languages') != -1:
                        n_flag = True
                        t_flag = False
                    elif v.text.find('Aliases') != -1:
                        n_flag = False
                        t_flag = True

                    if n_flag == True:
                        if 'title' in v.attrs.keys():
                            if v.attrs['title'].find('more') < 0:
                                nick[v.attrs['title']] = v.text
                    elif t_flag == True:
                        if 'title' in v.attrs.keys():
                            if v.attrs['title'].find('more') < 0:
                                trans[v.attrs['title']] = v.text
        data['nick'] = nick
        data['trans'] = trans
        data = str(data) + os.linesep
        data = bytes(data.encode('utf-8'))
        with open(path_w, 'ab+') as file:
            file.write(data)

    return None

# 작곡가 파일 Load
def get_name_from_html():
    with open(path, 'rb+') as file:
        data = file.read()
        data = str(data.decode())
        data = data.split(os.linesep)

        for v in data:
            v = v.split('^')
            get_nick_from_name(v[0], v[1])
    return None


path = 'ComposersLink.txt'
path = os.path.abspath(path)
path_w = 'ComposersName.txt'
path_w = os.path.abspath(path_w)

# get_name_from_yyy()
get_name_from_html()
