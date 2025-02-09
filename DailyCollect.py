import re
import requests
import datetime
import time
from time import time

def gettext(pid):
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    url = 'https://www.amazon.com/dp/'+pid
    s = requests.get(url, headers={'User-Agent':ua})
    return s

def getprice(s):
    pattern = '<span id="priceblock_ourprice" class="a-size-medium a-color-price">$'
    price = float(s.text.split(pattern)[-1].split('</span>')[0] )
    return int(price)

def getrevcnt(s):
    rc = re.findall('a-icon a-icon-star-.+\n.+\n', s.text)
    if rc != []:
        lrc = len(rc[0])
        if lrc>150:
            rcnt = re.findall('totalReviewCount">.+?</span', s.text)[0].split('>')[1].split('<')[0]
        else:
            rcnt = (rc[0].split('\n')[1].strip().split(' ')[0])
    else:
        print('rc={}'.format(len(rc)))
        lrc = len(rc)
        rcnt = rc
    return rcnt, lrc

def getinv(s):
    rc = re.findall('[\n]+.+Used & new</b> .+ from', s.text)
    if rc == []:
        rc = re.findall('[\n]+.+New</b> .+ from', s.text)
    if rc == []:
        rc = re.findall('[\n]+.+Used</b> .+ from', s.text)

    if rc != []:
        rc = rc[0].split('(')[1].split(')')[0]
    else:
        rc = ['NULL']
    return rc

def getrate(s, lrc):
    sr = []
    for i in range(1, 6):
        if lrc > 150:
            tmp = re.findall(str(i) +'star" aria-label=".+?%', s.text)
            if tmp != []:
                sr.append(tmp[0].split('="')[1].split('%')[0])
            else:
                sr.append(0)            
        else:
            tmp = re.findall(str(i) +' stars represent .+? of rating', s.text)
            if tmp != []:
                sr.append(tmp[0].split(str(i) +' stars represent ')[1].split('%')[0])
            else:
                sr.append(0)
    return sr

def logread():
    fn = "DailyCollection/items.txt"
    tar = open(fn, 'r')
    items = tar.read()
    tar.close()
    return items

def logwrite(lst):
    fn = "DailyCollection/DailyCollection.txt"
    tar = open(fn, 'a')
    r = len(lst)
    j = len(lst[0])-1
    #print('r={} j={}'.format(r, j))
    
    for q in range(r):
        for i in range(j):
            if i == 2: tar.write("'")
            tar.write('{}'.format(lst[q][i]))
            if i == 2: tar.write("'")
            tar.write(',')
        for i in range(5):
            #print('q={} i={}'.format(q, i))
            tar.write('{}'.format(lst[q][j][i]))
            if i < 4:
                tar.write(',')
        tar.write('\n')
    tar.close()

log = []
items = logread().split('\n')
for i in range(0, 14):
    log.append(items[i].split(','))
   
    log[i].append(str(datetime.datetime.now()))
    #print(log[i][1])
    
    s = gettext(log[i][1])
    log[i].append(getprice(s))
    rvcnt, lrc = getrevcnt(s)
    log[i].append(lrc)
    log[i].append(getinv(s))
    log[i].append(rvcnt)
    log[i].append(getrate(s, lrc))
    #print(log[i])
    
logwrite(log)