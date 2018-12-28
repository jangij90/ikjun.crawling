# encoding: utf-8


'''
author: Ikjun Jang
email: jangij90@gmail.com
'''


from subprocess import Popen


def test(index=None):
    c = 'python get_song.py ' + str(index)
    with Popen(c) as proc:
        end = proc.wait(timeout=None)
        if end == 0:
            return end
        else:
            return 1


def subprotest(count=None):

    i = 1

    while i < 28:
        result = test(i)
        if result == 0:
            i += 1
        else:
            print(i)
    return None


subprotest()
