# encoding: utf-8


'''
author: Ikjun Jang
email: jangij90@gmail.com
function: 작곡가별 곡 이름 가져오기
'''


import os
import re
import requests
import sys
import time

from bs4 import BeautifulSoup
from multiprocessing import Process

# 해당 작곡가의 다음 작곡페이지 확인
def get_next_categorypaginglink(html):
    time.sleep(1)
    categorypaginglink = None
    page_links = html.find_all('a', href=True, class_='categorypaginglink')
    for page_link in page_links:
        if 'next' in page_link.text:
            categorypaginglink = page_link['href']
            break
    return categorypaginglink

# 해당 작곡가의 총 작곡수 확인
def get_composition_len(html):
    lens = None
    compositions = html.find_all('span', id='catnummsgp1')
    if compositions:
        lens = str(compositions[0])
        lens = int(re.findall('\d+', lens)[1])
        return lens
    else:
        lens = 1
        return lens

# 작곡가 별 곡정보 가져 오기
def get_name_from_yyy(basecomposer=None, baselink=None, basenumber=None):
    path_w = str(Num) + '_' + str(basenumber) + '.txt'
    path_w = os.path.abspath(path_w)
    baseurl = 'http://imslp.org'
    compositions = None
    if baselink:
        title = None
        data = None
        i = 0

        resp = requests.get(baseurl + baselink)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')

            for v in soup.find_all('a', href=True, class_='categorypagelink'):
                if v.get_text(strip=True):
                    link = v['href']
                    title = v['title']
                    data = basecomposer + '^' + str(title) + '^' + str(link) + os.linesep
                    data = bytes(data.encode('utf-8'))
                    i += 1

                    with open(path_w, 'ab+') as file:
                        file.write(data)

    return None

# 작곡가별 나누기
def get_name_from_xxx(data, number):
    for v in data:
        if v:
            v = v.split('^')
            get_name_from_yyy(v[0], v[1], number)
    return None

# 정보가져오기
def get_info_from_compostion(tr=None):
    info = {}

    for v in tr:
        th = v.find_all('th')
        td = v.find_all('td')
        if not th:
            key = None
        else:
            key = th[0].text
            key = key.replace('\n','')
        if not td:
            value = None
        else:
            value = td[0].text
            value = value.replace('\n','')
        info[key] = value
    
    return info

# 곡명으로 곡정보 받아오기
def set_info_from_composition(basecomposer=None, baselink=None, basenumber=None):
    path_w = str(Num) + '_' + str(basenumber) + '_' + str(Num) + '.txt'
    path_w = os.path.abspath(path_w)
    baseurl = 'http://imslp.org'
    if baselink:
        data = {}
        resp = requests.get(baseurl + baselink)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')

            tr = soup.select('div.wi_body tr')
            info = get_info_from_compostion(tr)

            data[basecomposer] = info
            data = str(data) + os.linesep
            data = bytes(data.encode('utf-8'))
            with open(path_w, 'ab+') as file:
                file.write(data)

            return None
            
    return None

# 곡목록에서 곡명 받아오기
def get_composition_from_composer(path=None, Number=None):

    with open(path, 'rb+') as file:
        data = file.read()
        data = str(data.decode())
        data = data.split(os.linesep)
        for index, v in enumerate(data):
            if v:
                v = v.split('^')
                set_info_from_composition(v[0], v[2], Number)
                
    return None

# sys.argv[1]
Num = 2  # sys.argv[1]

if __name__ == '__main__':

    # 곡정보 가져오기
    path = str(Num) + '.txt'
    procs = []
    for v in range(1, 4):
        path = str(Num) + '_' + str(v) + '.txt'
        # get_composition_from_composer(path, v)
        proc = Process(target=get_composition_from_composer, args=(path, v,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    # 200곡씩 곡담기
    # path = os.path.abspath(path)
    # a = []
    # b = []
    # i = 0
    # with open(path, 'rb+') as file:
    #     data = file.read()
    #     data = str(data.decode())
    #     data = data.split(os.linesep)

    #     for v in data:  # 600
    #         a.append(v)
    #         i += 1
    #         if i == 200:
    #             b.append(a)
    #             i = 0
    #             a = []
    #     if a:
    #         b.append(a)

    #     j = 1
    #     for v in b:
    #         proc = Process(target=get_name_from_xxx, args=(v, j,))
    #         procs.append(proc)
    #         proc.start()
    #         j += 1
    #     for proc in procs:
    #         proc.join()
