# encoding: utf-8


'''
author: Ikjun Jang
email: jangij90@gmail.com
function: 작곡가별 곡명 합치기
'''


import os
import re
import requests
import time

from bs4 import BeautifulSoup

# 합치기(하나의 파일로 Save)
def combine_composition_from_file(file):
    data = file.read()
    data = str(data.decode())
    data = data.split(os.linesep)

    for v in data:
        if v:
            resist = v.split('^')
            a = resist[1].split(' (')

            resist = resist[0] + '^' + a[0] + '^' + resist[2] + os.linesep
            resist = bytes(resist.encode('utf-8'))

            with open(path, 'ab+') as files:
                files.write(resist)

# 합치기(개별 파일 Load)
def set_combine_from_composition():

    for i in range(1, 28):
        for j in range(1, 4):
            path_r = str(i) + '_' + str(j) + '.txt'
            path_r = os.path.abspath(path_r)
            with open(path_r, 'rb+') as file:
                combine_composition_from_file(file)
    return None

# 나누기(600개씩 개별 파일로 Save)
def set_share_from_composition():
    path_r = 'ComposersLink.txt'
    path_r = os.path.abspath(path_r)
    with open(path_r, 'rb+') as file:
        data = file.read()
        data = str(data.decode())
        data = data.split(os.linesep)
        i = 0
        j = 1
        for v in data:
            i += 1
            v = v + os.linesep
            v = bytes(v.encode('utf-8'))
            path_w = str(j) + '.txt'
            path_w = os.path.abspath(path_w)
            with open(path_w, 'ab+') as file:
                file.write(v)
            if i == 600:
                i = 0
                j += 1
        return None

path = 'composition.txt'
path = os.path.abspath(path)

set_combine_from_composition()
# set_share_from_composition()
