
import random
import requests
import time
import urllib

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from multiprocessing import Pool
from lxml.html import fromstring
import os, sys
import shutil

def search(url):
    browser = webdriver.Chrome(os.getcwd()+'/chromedriver')
    print(os.getcwd()+'/chromedriver')
    browser.get(url)
    time.sleep(1)

    element = browser.find_element_by_tag_name("body")

    for i in range(80):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    browser.find_element_by_id("smb").click()

    for i in range(50):
         element.send_keys(Keys.PAGE_DOWN)
         time.sleep(0.2)

    time.sleep(1)

    source = browser.page_source
    browser.close()
    print("1")
    return source

def download_image(link):

    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    num = random.randrange(1, 1000)
    filname = str(num)

    try:
        r = requests.get("https://www.google.com" + link.get("href"), headers=headers)
    except:
        print("Cannot get link.")
    title = str(fromstring(r.content).findtext(".//title"))
    link = title.split(" ")[-1]

    print("At : " + os.getcwd() + ", Downloading from " + link)

    try:
        if link.split(".")[-1] == ('jpg' or 'png' or 'jpeg'):

            #urllib.request.urlretrieve(link, link.split("/")[-1])
            urllib.request.urlretrieve(link, filname + '.jpg')
    except:
        pass

def start(ttk):


    sys.setrecursionlimit(20000)

    # query = args.keyword
    query = ttk

    url = "https://www.google.co.kr/search?q=" + query + "&rlz=1C1CHBD_koKR813KR813&source=lnms&tbm=isch&sa=X&ved=0ahUKEwirn8mLxKXdAhWZIIgKHUdfBRkQ_AUICigB&biw=1280&bih=610"
    source = search(url)

    soup = BeautifulSoup(str(source), "html.parser")
    #ua = UserAgent()


    if not os.path.isdir(query):
        if os.path.isdir("crawlingResult"):
            shutil.rmtree("crawlingResult")
        os.makedirs("crawlingResult")
        os.chdir(str(os.getcwd()) + "/" + "crawlingResult")
        links = soup.find_all("a", class_="rg_l")

    with Pool() as pool:
        # pool.map(download_image, links)
        pool = Pool(processes=4)
        try:
            pool.map(download_image, links)
        except Exception as e:
            print(str(e))