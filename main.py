import sys
from selenium import webdriver
import requests
from lxml import html
import http.client

def _safe_read(self, amt): #继承，解决Chunk问题
        s = []
        while amt > 0:
            chunk = self.fp.read(min(amt, MAXAMOUNT))
            #if not chunk:
                #raise IncompleteRead(b''.join(s), amt)
            s.append(chunk)
            amt -= len(chunk)
        return b"".join(s)

def get_jumpurl():
    global JUMPURL
    driver = webdriver.Chrome('./chromedriver.exe')
    URL = sys.argv[1]
    driver.get(URL)
    el = driver.find_element_by_xpath('//*[@id="resource-box"]/div/div/h3/a')
    JUMPURL = el.get_attribute('href')
    driver.close()


def get_tags():
    global tags,tree,page
    headers = { 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4)AppleWebKit/537.36(KHTML,likeGecko)Chrome/44.0.2403.157 Safari/537.36',    'Connection':'keep-alive','Accept-Encoding':'gzip, deflate'}
    page = requests.get(JUMPURL,headers = headers).text
    tree = html.fromstring(page)
    count1 = 1
    count2 = 1
    tag_1 = []
    tags = []
    seasons = len(tree.xpath('//*[@id="menu"]/li'))
    if seasons != 1:
        while count2 <= seasons:
            while count1 <= len(tree.xpath('//*[@id="sidetab-%d"]/ul/li' % count2)):
                try:
                    el = tree.xpath('//*[@id="sidetab-%d"]/ul/li[%d]/a/span' % (count2, count1))[0]
                    tag_t = tree.xpath('//*[@id="sidetab-%d"]/ul/li[%d]/a/@aria-controls' % (count2, count1))[0]
                    tag_1.append(tag_t)
                    break
                    count1 = count1 + 1
                except:
                    count1 = count1 + 1
                finally:
                    pass
            count2 = count2 + 1
            count1 = 1
    else:
        tab = tree.xpath('//*[@id="menu"]/li/a/@aria-controls')[0]
        while count1 <= len(tree.xpath('//*[@id="%s"]/ul/li' % tab)):
            try:
                el = tree.xpath('//*[@id="%s"]/ul/li[%d]/a/span' % (tab, count1))[0]
                tag_t = tree.xpath('//*[@id="%s"]/ul/li[%d]/a/@aria-controls' % (tab, count1))[0]
                tag_1.append(tag_t)
                break
                count1 = count1 + 1
            except:
                count1 = count1 + 1
            finally:
                pass
    for s in tag_1:
        s = '"' + s + '"'
        tags.append(s)


def get_ed2kurl():
    global list_1
    list_1 = []
    lenth = len(tags)
    x = 1
    y = 0
    el = tree.xpath('//*[@id='+tags[y]+']/ul/li[%d]/ul/li[2]/a/@href' % x)
    while y < lenth:
        while el != []:
            if type(el) == list : list_1.append(str(el[0].encode('utf-8'),encoding='utf-8'))
            x = x + 1
            el = tree.xpath('//*[@id=' + tags[y] + ']/ul/li[%d]/ul/li[2]/a/@href' % x)
        el = None
        x = 0
        y = y +1


print('Getting Url of downloading page...')
get_jumpurl()
print('Getting tags...')
get_tags()
print('Getting ed2k links...')
get_ed2kurl()


for i in list_1:
    print(i)
