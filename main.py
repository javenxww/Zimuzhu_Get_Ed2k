# coding:utf-8
import sys
from selenium import webdriver
import requests
from lxml import html
import platform

OS = platform.platform()

def get_jumpurl():
    global JUMPURL
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    if "Windows" in OS:
        driver = webdriver.Chrome('./chromedriver.exe',chrome_options=option)
    if "Linux" in OS:
        driver = webdriver.Chrome('./chromedriver_linux',chrome_options=option)
    if "Darwin" in OS or "Mac" in OS:
        driver = webdriver.Chrome('./chromedriver_macos',chrome_options=option)
    URL = sys.argv[1]
    driver.get(URL)
    el = driver.find_element_by_xpath('//*[@id="resource-box"]/div/div/h3/a')
    JUMPURL = el.get_attribute('href')
    driver.close()


def get_tags():
    global tags,tree,page
    headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    page = requests.get(JUMPURL,headers = headers,stream=True).text
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
    global ed2kurl
    ed2kurl = []
    lenth = len(tags)
    x = 1
    y = 0
    el = tree.xpath('//*[@id='+tags[y]+']/ul/li[%d]/ul/li[2]/a/@href' % x)
    while y < lenth:
        while el != []:
            if type(el) == list : ed2kurl.append(str(el[0].encode('utf-8'),encoding='utf-8'))
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


for i in ed2kurl:
    print(i)
