# -*- coding: utf-8 -*-
from __future__ import division, generators
from PIL import ImageTk
import tkinter as tk
import tkinter.messagebox
from tkinter import *
import glob
import cv2
import numpy as np
import time
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import shutil
import random
from PIL import Image
import subprocess

SIZE = 200, 200
COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']
from six.moves import queue


# import matplotlib
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure

# ------------------------------------------------------------------------
# Audio 마이크 스트림 받는 클래스
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# GUI 클래스 시작
# ------------------------------------------------------------------------

class SampleApp(tk.Tk):
    select_word = None
    labels = None
    word2vec_model = "./enwiki_5_ner.txt"
    num = 0
    choices = ['aeroplane', 'apple',
               'backpack', 'banana', 'baseball glove', 'baseball bat', 'bear', 'bed', 'bench', 'bicycle', 'bird',
               'boat', 'book', 'bottle', 'bowl', 'broccoli', 'bus',
               'cake', 'car', 'carrot', 'cat', 'cell phone', 'chair', 'clock', 'cow', 'cup',
               'diningtable', 'dog', 'donut',
               'elephant',
               'fire hydrant', 'fork', 'frisbee',
               'giraffe',
               'hair drier', 'handbag', 'horse', 'hot dog',
               'keyboard', 'kite', 'knife'
                                   'laptop',
               'microwave', 'motorbike', 'mouse',
               'orange', 'oven',
               'parkingmeter', 'person', 'pizza', 'pottedplant',
               'refrigerator', 'remote',
               'sandwich', 'scissors', 'sheep', 'sink', 'stop sign', 'skateboard', 'skis', 'sofa', 'spoon',
               'sports ball', 'suitcase', 'surfboard', 'snowboard'
                                                       'teddy bear', 'tennis racket', 'tie', 'toaster', 'toilet',
               'toothbrush', 'train', 'traffic light', 'truck', 'tvmonitor',
               'umbrella',
               'vase',
               'wine glass',
               'zebra'
               ]

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('CIC')
        self.geometry('750x680')
        # audio process
        self.audio_process = None
        self.audio_result = ""

        # initialize global state
        self.imageDir = ''
        self.imageList = []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.wig_textBox = 0
        self.egPanel = tk.Frame(self, border=10)
        # self.egPanel.grid(row=1, column=0, rowspan=5, sticky=tk.N)
        self.egLabels = []
        for i in range(6):
            self.egLabels.append(tk.Label(self.egPanel))
            self.egLabels[-1].pack(side=tk.TOP)

        # 검색바
        # self.frame_topEntry = tk.Entry(self)
        self.original_btn = tk.Button(self, text=' Original ', command=self.msg_ori, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.gray_btn = tk.Button(self, text=' Gray ', command=self.msg_gray, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.bilateral_btn = tk.Button(self, text=' Bilateral ', command=self.msg_bilater, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.blur_btn = tk.Button(self, text=' Blur ', command=self.msg_bluring, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.median_btn = tk.Button(self, text=' Median ', command=self.msg_median, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.gaussian_btn = tk.Button(self, text=' Gaussian ', command=self.msg_gaussian, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.detail_btn = tk.Button(self, text=' Detail ', command=self.msg_detail, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.homomor_btn = tk.Button(self, text=' Hormomor ', command=self.msg_hormomorphic, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.pencil_btn = tk.Button(self, text=' Pencil ', command=self.msg_pencil, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.stylization_btn = tk.Button(self, text=' Stylization ', command=self.msg_stylization, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.erosion_btn = tk.Button(self, text=' Erosion ', command=self.msg_erosion, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.dilation_btn = tk.Button(self, text=' Dilation ', command=self.msg_dilation, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.binary_btn = tk.Button(self, text=' Binary ', command=self.msg_binary, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.binaryinv_btn = tk.Button(self, text=' BinaryINV ', command=self.msg_binaryinv, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.trunc_btn = tk.Button(self, text=' Trunc ', command=self.msg_trunc, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.tozero_btn = tk.Button(self, text=' Tozero ', command=self.msg_tozero, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.tozeroinv_btn = tk.Button(self, text=' TozeroINV ', command=self.msg_tozeroinv, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.adthmean_btn = tk.Button(self, text=' AD.Mean ', command=self.msg_adthmean, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.adthgaus_btn = tk.Button(self, text=' AD.Gau ', command=self.msg_adthgaus, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.otsu_btn = tk.Button(self, text=' Otsu ', command=self.msg_otsu, font=("나눔스퀘어 Bold", 10), height=3, width=9)
        self.resize_btn = tk.Button(self, text=' Resize ', command=self.msg_resize, font=("나눔스퀘어 Bold", 10), height=3, width=43)

        self.lb = tk.Label(self, text='--------------------- Filter ----------------------', font=("나눔스퀘어 Bold", 10))
        self.lb_row = tk.Label(self, text='가로 : ', font=("나눔스퀘어 Bold", 10))
        self.lb_col = tk.Label(self, text='세로 : ', font=("나눔스퀘어 Bold", 10))
        self.row_textBox = tk.Entry(self, width='5', font=("나눔스퀘어 Bold", 25))
        self.col_textBox = tk.Entry(self, width='5', font=("나눔스퀘어 Bold", 25))

        # 다운개수
        # self.count = tk.Label(self, text='다운개수 입력(10이상)', font=("나눔스퀘어 Bold", 10))
        # self.wig_textBox1 = tk.Entry(self, width='7', font=("나눔스퀘어 Bold", 25))
        # self.wig_textBox1.focus_set()
        # 검색창
        self.lb1 = tk.Label(self, text='검색 단어 입력', font=("나눔스퀘어 Bold", 10))
        self.wig_textBox = tk.Entry(self, width='15', font=("나눔스퀘어 Bold", 25))

        self.wig_textBox.bind("<Return>", lambda event, a="enter": self.enter_save_data(a))
        # make sure the frame has focus so the binding will work
        self.wig_textBox.focus_set()

        # 검색버튼
        self.search_btn = tk.Button(self, text='검색', font=("나눔스퀘어 Bold", 15), command=self.save_data)
        # self.testt = tk.Button(self, text='테스트', command=self.loadDir)
        # self.frame_list = tk.Entry(self)
        # self.list = tk.Listbox(self.frame_list, font=("Consolas"))

        # 리스트
        frame1 = Frame(self)
        frame1.pack()
        self.list = tk.Listbox(self, width='30', height='29', font=("Consolas"))
        self.list.pack(fill="both")
        for li in self.choices:
            self.list.insert(tk.END, li)
        # 스크롤바
        # self.scrollbar = tk.Scrollbar(self)
        # self.scrollbar.config(command=self.list.yview)
        #
        # self.scrollbar.pack(side="right", fill="y")
        #
        # self.list.config(yscrollcommand=self.scrollbar.set)

        # self.imageList = tk.Listbox(self, width='40', height='27', font=("Consolas"))

        # 클래스 검색
        self.searchClass = tk.Listbox(self, width='30', height=1, font=("Consolas"))

        self.original_btn.place(x=40, y=110)
        self.gray_btn.place(x=130, y=110)
        self.bilateral_btn.place(x=220, y=110)
        self.detail_btn.place(x=310, y=110)
        self.blur_btn.place(x=40, y=180)
        self.median_btn.place(x=130, y=180)
        self.gaussian_btn.place(x=220, y=180)
        self.homomor_btn.place(x=310, y=180)
        self.pencil_btn.place(x=40, y=250)
        self.stylization_btn.place(x=130, y=250)
        self.erosion_btn.place(x=220, y=250)
        self.dilation_btn.place(x=310, y=250)
        self.binary_btn.place(x=40, y=320)
        self.binaryinv_btn.place(x=130, y=320)
        self.trunc_btn.place(x=220, y=320)
        self.tozero_btn.place(x=310, y=320)
        self.tozeroinv_btn.place(x=40, y=390)
        self.adthmean_btn.place(x=130, y=390)
        self.adthgaus_btn.place(x=220, y=390)
        self.otsu_btn.place(x=310, y=390)
        self.resize_btn.place(x=40, y=500)

        self.lb.place(x=40, y=90)
        self.lb_row.place(x=40, y=570)
        self.row_textBox.place(x=80, y=560)
        self.lb_col.place(x=220, y=570)
        self.col_textBox.place(x=260, y=560)

        # self.count.place(x=40, y=20)
        # self.wig_textBox1.place(x=40, y=40)
        self.lb1.place(x=40, y=30)
        self.wig_textBox.place(x=40, y=50)


        self.search_btn.place(x=330, y=50)
        self.list.place(x=430, y=73)
        # self.imageList.place(x=40, y=90)
        self.searchClass.place(x=430, y=50)
        # self.scrollbar.place(x=703, y=83)
        # -----------------
        # End Position
        # -----------------

    # ------------------------------------------------------------------------
    # Functions
    # ------------------------------------------------------------------------
    def search(self, googleUrl, naverUrl):
        # 구글 크롬실행
        googleBrowser = webdriver.Chrome(os.getcwd() + '/chromedriver')
        print(os.getcwd() + '/chromedriver')
        googleBrowser.get(googleUrl)
        time.sleep(1)

        # # 네이버 크롬실행
        # naverBrowser = webdriver.Chrome(os.getcwd() + '/chromedriver')
        # print(os.getcwd() + '/chromedriver')
        # naverBrowser.get(naverUrl)
        # time.sleep(1)

        googleElement = googleBrowser.find_element_by_tag_name("body")
        # naverElement = naverBrowser.find_element_by_tag_name("body")

        # 구글 스크롤 다운
        for i in range(80):
            googleElement.send_keys(Keys.PAGE_DOWN)
            # naverElement.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
        try:
            googleBrowser.find_element_by_id("smb").click()
        except:
            print("no button")
        # naverBrowser.find_element_by_class_name("btn_more").click()

        for i in range(50):
            googleElement.send_keys(Keys.PAGE_DOWN)
            # naverElement.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        time.sleep(1)

        source = googleBrowser.page_source #+ naverBrowser.page_source
        googleBrowser.close()
        # naverBrowser.close()
        print("browser close")
        return source


    # def navsearch(self, url):
    #     browser = webdriver.Chrome(os.getcwd() + '/chromedriver')
    #     print(os.getcwd() + '/chromedriver')
    #     browser.get(url)
    #     time.sleep(1)
    #
    #     element = browser.find_element_by_tag_name("body")
    #
    #     for i in range(80):
    #         element.send_keys(Keys.PAGE_DOWN)
    #         time.sleep(0.2)
    #
    #     browser.find_element_by_class_name("btn_more").click()
    #
    #     for i in range(50):
    #         element.send_keys(Keys.PAGE_DOWN)
    #         time.sleep(0.2)
    #
    #     time.sleep(1)
    #
    #     source = browser.page_source
    #     browser.close()
    #     print("1")
    #     return source



    # 이미지 다운로드 진행
    def download_image(self, bb):
        name = random.randrange(1, 100000)
        fullName = str(name) + ".jpg"
        outpath = str(os.getcwd()) + "/"
        # urllib.request.urlretrieve(bb, outpath + fullName)

        try:
            urllib.request.urlretrieve(bb, outpath + fullName)
        except:
            print("None")
        # time.sleep(1)            # 가끔 타임아웃걸려서 일단 1초 텀둠


    def start(self, ttk):


        query = ttk

        url = "https://www.google.co.kr/search?q=" + query + "&rlz=1C1CHBD_koKR813KR813&source=lnms&tbm=isch&sa=X&ved=0ahUKEwirn8mLxKXdAhWZIIgKHUdfBRkQ_AUICigB&biw=1280&bih=610"
        naverurl = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=" + query


        source = self.search(url, naverurl)


        soup = BeautifulSoup(str(source), "html.parser")
        #ua = UserAgent()
        links = []

        if not os.path.isdir(query):
            if os.path.isdir("crawlingResult"):
                shutil.rmtree("crawlingResult")
            os.makedirs("crawlingResult")
            os.chdir(str(os.getcwd()) + "/" + "crawlingResult")
            links = soup.find_all("img")

        print(len(links))

        for c in links:
            print(c.get('src'))
            self.download_image(c.get('src'))

        # for c in range(10,len(links)):
        #     print(links[c].get('src'))
        #     self.download_image(links[c].get('src'))

        print("#####################################################################")
        print("finish")
        print("#####################################################################")
    # ------------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------------
    def textSave(self):
        f = open(os.getcwd() + "/label.txt", 'w')
        f.write(self.wig_textBox.get())

    def loadDir(self, dbg=True):

        s = r'D:\workspace\python\labelGUI'

        self.cur = 1
        # self.total = len(self.imageList)

        # set up output dir
        self.outDir = os.path.join(r'./Labels', '%03d' % (int(self.wig_textBox.get())))
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        print(self.wig_textBox.get())
        # load example bboxes
        # self.egDir = os.path.join(r'./Examples', '%03d' % (self.category))
        self.egDir = os.path.join(r'./Examples', '%03d' % (int(self.wig_textBox.get())))
        if not os.path.exists(self.egDir):
            return
        filelist = glob.glob(os.path.join(self.egDir, '*.JPEG'))
        print(filelist)
        self.tmp = []
        self.egList = []
        random.shuffle(filelist)
        for (i, f) in enumerate(filelist):
            if i == 6:
                break
            im = Image.open(f)
            r = min(SIZE[0] / im.size[0], SIZE[1] / im.size[1])
            new_size = int(r * im.size[0]), int(r * im.size[1])
            self.tmp.append(im.resize(new_size, Image.ANTIALIAS))
            self.egList.append(ImageTk.PhotoImage(self.tmp[-1]))
            self.egLabels[i].config(image=self.egList[-1], width=SIZE[0], height=SIZE[1])

        self.loadImage()
        print
        '%d images loaded from %s' % (self.total, s)

    def loadImage(self):
        # load image
        print('loadImage')
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width=max(self.tkimg.width(), 400), height=max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image=self.tkimg)  # anchor=NW
        self.progLabel.config(text="%04d/%04d" % (self.cur, self.total))

        # load labels
        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        bbox_cnt = 0
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        bbox_cnt = int(line.strip())
                        continue
                        tmp = [int(t.strip()) for t in line.split()]
                        ##                    print tmp
                        self.bboxList.append(tuple(tmp))
                        tmpId = self.mainPanel.create_rectangle(tmp[0], tmp[1], \
                                                                tmp[2], tmp[3], \
                                                                width=2, \
                                                                outline=COLORS[(len(self.bboxList) - 1) % len(COLORS)])
                        self.bboxIdList.append(tmpId)
                        self.listbox.insert(END, '(%d, %d) -> (%d, %d)' % (tmp[0], tmp[1], tmp[2], tmp[3]))
                        self.listbox.itemconfig(len(self.bboxIdList) - 1,
                                                fg=COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])

    # enter search
    def enter_save_data(self, a):
        # self.loadDir()
        print(a)
        print(os.getcwd())
        yolo_path = 'yolo/build/darknet/x64/darknet.exe'

        self.textSave()
        print(self.wig_textBox.get())
        self.start(self.wig_textBox.get())
        os.chdir("../")
        # ctypes.windll.shell32.ShellExecuteA(0, 'open', yolo_path, None, None,1)
        subprocess.call(yolo_path)

    # button search
    def save_data(self):
        # self.loadDir()

        print(os.getcwd())
        yolo_path = 'yolo/build/darknet/x64/darknet.exe'

        self.textSave()
        print(self.wig_textBox.get())
        self.start(self.wig_textBox.get())
        os.chdir("../")
        # ctypes.windll.shell32.ShellExecuteA(0, 'open', yolo_path, None, None,1)
        subprocess.call(yolo_path)

    def msg_resize(self):
        name = '_' + self.row_textBox.get() + '_' + self.col_textBox.get()
        filename = "result"
        filename2 = filename + name

        row_s = self.row_textBox.get()
        col_s = self.col_textBox.get()
        row_n = int(row_s)
        col_n = int(col_s)

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            dim = (row_n, col_n)
            res = cv2.resize(cv2.imread(i), dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite((filename2 + '/%d_resize.jpg' % number), res)
            cv2.waitKey(0)

        tk.messagebox.showwarning("메세지 상자", "Resizing 완료하였습니다.")
        pass

        # Original 버튼 클릭시

    def msg_ori(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_ori()
        else:
            return False
        pass

    # Stylization 버튼 클릭시
    def msg_stylization(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_stylization()
            else:
                return False
        pass


    # Erosion 버튼 클릭시
    def msg_erosion(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_erosion()
            else:
                return False
        pass

    # Dilation 버튼 클릭시
    def msg_dilation(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_dilation()
            else:
                return False
        pass

    # Binary 버튼 클릭시
    def msg_binary(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_binary()
            else:
                return False
        pass

    # BinaryINV 버튼 클릭시
    def msg_binaryinv(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_binaryinv()
            else:
                return False
        pass

    # Trunc 버튼 클릭시
    def msg_trunc(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_trunc()
            else:
                return False
        pass

    # Tozero 버튼 클릭시
    def msg_tozero(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_tozero()
            else:
                return False
        pass

    # TozeroINV 버튼 클릭시
    def msg_tozeroinv(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_tozeroinv()
            else:
                return False
        pass

    # Adthmean 버튼 클릭시
    def msg_adthmean(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_adthmean()
            else:
                return False
        pass


    # Adthgaus 버튼 클릭시
    def msg_adthgaus(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_adthgaus()
            else:
                return False
        pass

    # Otsu 버튼 클릭시
    def msg_otsu(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_otsu()
            else:
                return False
        pass

    # Pencil 버튼 클릭시
    def msg_pencil(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_pencil()
            else:
                return False
        pass

    # Detail 버튼 클릭시
    def msg_detail(self):
        if len(self.wig_textBox.get()) == 0:
            tk.messagebox.showwarning("메세지 상자", "텍스트 상자가 비어있습니다.")
        else:
            tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
            if tmp is True:
                self.ok_detail()
            else:
                return False
        pass

    def ok_ori(self):
        filename = os.getcwd() + "/result"
        filename2 = filename + '_ori'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            ori = cv2.imread(i, cv2.IMREAD_COLOR)
            cv2.imwrite((filename + '_ori/%d_ori.jpg' % number), ori)
            cv2.waitKey(0)
        pass

    # Gray 버튼 클릭시
    def msg_gray(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_gray()
        else:
            return False
        pass

    def ok_gray(self):
        filename = "result"
        filename2 = filename + '_gray'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            gray = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
            cv2.imwrite((filename + '_gray/%d_gray.jpg' % number), gray)
            cv2.waitKey(0)
        pass

    # Unchange 버튼 클릭시
    def msg_unchange(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_unchange()
        else:
            return False
        pass

    def ok_unchange(self):
        filename = "result"
        filename2 = filename + '_unchange'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            unchange = cv2.imread(i, cv2.IMREAD_UNCHANGED)
            cv2.imwrite((filename + '_unchange/%d_unchange.jpg' % number), unchange)
            cv2.waitKey(0)
        pass

    # Blur 버튼 클릭시
    def msg_bluring(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_bluring()
        else:
            return False
        pass

    def ok_bluring(self):
        filename = "result"
        filename2 = filename + '_blur'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            blur = cv2.blur(cv2.imread(i), (5, 5))
            cv2.imwrite((filename + '_blur/%d_blur.jpg' % number), blur)
            cv2.waitKey(0)
            pass

    def msg_median(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_median()
        else:
            return False
        pass

    def ok_median(self):
        filename = "result"
        filename2 = filename + '_median'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            median = cv2.medianBlur(cv2.imread(i), 5)
            cv2.imwrite((filename + '_median/%d_median.jpg' % number), median)
            cv2.waitKey(0)
        pass

    def msg_gaussian(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_gaussian()
        else:
            return False
        pass

    def ok_gaussian(self):
        filename = "result"
        filename2 = filename + '_gaussian'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            gaussian = cv2.GaussianBlur(cv2.imread(i), (5, 5), 0)
            cv2.imwrite((filename + '_gaussian/%d_gaussian.jpg' % number), gaussian)
            cv2.waitKey(0)
            pass

    # bilater 버튼 클릭시
    def msg_bilater(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_bilater()
        else:
            return False
        pass

    def ok_bilater(self):
        filename = "result"
        filename2 = filename + '_bilateral'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            number = number + 1
            bilateral = cv2.bilateralFilter(cv2.imread(i), 9, 75, 75)
            cv2.imwrite((filename + '_bilateral/%d_bilateral.jpg' % number), bilateral)
            cv2.waitKey(0)
        pass

    # Hormomorphic 버튼 클릭시
    def msg_hormomorphic(self):
        tmp = tk.messagebox.askokcancel("메세지 상자", "필터 적용을 하시겠습니까?\n적용시 '확인'을 눌러주세요")
        if tmp is True:
            self.ok_hormomorphic()
        else:
            return False
        pass

    def ok_hormomorphic(self):
        filename = "result"
        filename2 = filename + '_homomorphic'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            homomorphic = cv2.cvtColor(cv2.imread(i), cv2.COLOR_BGR2YUV)
            number = number + 1
            cv2.imwrite((filename + '_homomorphic/%d_homomorphic.jpg' % number), homomorphic)
            cv2.waitKey(0)
        pass

    def ok_pencil(self):
        filename = "result"
        filename2 = filename + '_pencil'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            pencil = cv2.pencilSketch(cv2.imread(i), sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            number = number + 1
            cv2.imwrite((filename + '_pencil/%d_pencil.jpg' % number), pencil)
            cv2.waitKey(0)
        pass

    def ok_stylization(self):
        filename = "result"
        filename2 = filename + '_stylization'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            stylization = cv2.stylization(cv2.imread(i), sigma_s=60, sigma_r=0.07)
            number = number + 1
            cv2.imwrite((filename + '_stylization/%d_stylization.jpg' % number), stylization)
            cv2.waitKey(0)
        pass

    def ok_erosion(self):
        filename = "result"
        filename2 = filename + '_erosion'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        kernel = np.ones((3, 3), np.unit8)

        for i in files_img:
            erosion = cv2.erode(cv2.imread(i), kernel, iterations=1)
            number = number + 1
            cv2.imwrite((filename + '_erosion/%d_erosion.jpg' % number), erosion)
            cv2.waitKey(0)
        pass

    def ok_dilation(self):
        filename = "result"
        filename2 = filename + '_dilation'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        kernel = np.ones((3, 3), np.unit8)

        for i in files_img:
            dilation = cv2.dilate(cv2.imread(i), kernel, iterations=1)
            number = number + 1
            cv2.imwrite((filename + '_dilation/%d_dilation.jpg' % number), dilation)
            cv2.waitKey(0)
        pass

    def ok_binary(self):
        filename = "result"
        filename2 = filename + '_binary'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            binary = cv2.threshold(cv2.imread(i), 127, 255, cv2.THRESH_BINARY)
            number = number + 1
            cv2.imwrite((filename + '_binary/%d_binary.jpg' % number), binary)
            cv2.waitKey(0)
        pass

    def ok_binaryinv(self):
        filename = "result"
        filename2 = filename + '_binaryinv'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            binaryinv = cv2.threshold(cv2.imread(i), 127, 255, cv2.THRESH_BINARY_INV)
            number = number + 1
            cv2.imwrite((filename + '_binaryinv/%d_binaryinv.jpg' % number), binaryinv)
            cv2.waitKey(0)
        pass

    def ok_trunc(self):
        filename = "result"
        filename2 = filename + '_trunc'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            trunc = cv2.threshold(cv2.imread(i), 127, 255, cv2.THRESH_TRUNC)
            number = number + 1
            cv2.imwrite((filename + '_trunc/%d_trunc.jpg' % number), trunc)
            cv2.waitKey(0)
        pass

    def ok_tozero(self):
        filename = "result"
        filename2 = filename + '_tozero'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            tozero = cv2.threshold(cv2.imread(i), 127, 255, cv2.THRESH_TOZERO)
            number = number + 1
            cv2.imwrite((filename + '_tozero/%d_tozero.jpg' % number), tozero)
            cv2.waitKey(0)
        pass

    def ok_tozeroinv(self):
        filename = "result"
        filename2 = filename + '_homomorphic'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            tozeroinv = cv2.threshold(cv2.imread(i), 127, 255, cv2.THRESH_TOZERO_INV)
            number = number + 1
            cv2.imwrite((filename + '_tozeroinv/%d_tozeroinv.jpg' % number), tozeroinv)
            cv2.waitKey(0)
        pass

    def ok_adthmean(self):
        filename = "result"
        filename2 = filename + '_adthmean'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            adthmean = cv2.adaptiveThreshold(cv2.imread(i), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            number = number + 1
            cv2.imwrite((filename + '_adthmean/%d_adthmean.jpg' % number), adthmean)
            cv2.waitKey(0)
        pass

    def ok_adthgaus(self):
        filename = "result"
        filename2 = filename + '_adthgaus'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            adthgaus = cv2.adaptiveThreshold(cv2.imread(i), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            number = number + 1
            cv2.imwrite((filename + '_adthgaus/%d_adthgaus.jpg' % number), adthgaus)
            cv2.waitKey(0)
        pass

    def ok_otsu(self):
        filename = "result"
        filename2 = filename + '_otsu'

        if not os.path.isdir(filename2):
            os.mkdir(filename2)

        files = os.listdir(filename)
        files_img = [filename + "/" + i for i in files if i.endswith('jpg' or 'png' or 'jpeg')]
        number = 0

        for i in files_img:
            otsu = cv2.threshold(cv2.imread(i), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            number = number + 1
            cv2.imwrite((filename + '_otsu/%d_otsu.jpg' % number), otsu)
            cv2.waitKey(0)
        pass


    # 녹음 버튼 클릭시
    def button_sound(self):
        self.lb4['text'] = '음성 녹음 \n\n켜짐'
        self.lb4['fg'] = 'white'
        self.lb4['bg'] = 'red'
        self.after(100, self.voice_recognition)
        pass

    # 검색 단어 입력 부분 단어가 변경 시
    def change_text(self, event):
        flag = self.wig_textBox.edit_modified()
        if flag:
            txt = self.wig_textBox.get("1.0", tk.END)
            # word2vec
            self.wig_listProcess1.delete('0', 'end')
            self.wig_listResult.delete('0', 'end')
            results, words = self.find_matching(txt)
            for word, index in zip(words, range(len(words))):
                self.wig_listProcess1.insert('end', str(word))
                if index == 9:
                    break
            for result in results:
                self.wig_listResult.insert('end', str(result))

            # fuzz
            self.wig_listProcess2.delete('0', 'end')
            self.wig_listResult2.delete('0', 'end')
            result = self.fuzz_match(txt)
            if result[0][1] is 0:
                self.wig_listProcess2.insert('end', '단어를 찾을 수 없음')
                self.wig_listResult2.insert('end', '단어를 찾을 수 없음')
            else:
                for i in range(10):
                    self.wig_listProcess2.insert('end', result[i][0] + ' - ' + str(result[i][1]))
                self.wig_listResult2.insert('end', result[0][0])

        self.wig_textBox.edit_modified(False)
        pass

    # 리스트에서 단어 선택 시
    def select_list(self, event):
        try:
            widget = event.widget
            index = widget.curselection()[0]
            value = widget.get(index)
            self.select_word = value
            print("selection: %d" % index + ": '%s'" % value)
        except Exception as e:
            print(e)
        pass




# ------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------

if __name__ == '__main__':
    app = SampleApp()
    app.mainloop()
