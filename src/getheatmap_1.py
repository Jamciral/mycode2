"""
2021/7/22
@author: 张新宇
读取pdf文件并生成键盘热力图(1_heatmap.jpg)、按键使用频率柱状图(1_letter_freq_bar.jpg)以及文件文本的拼音形式(1_共产党宣言_拼音.txt)
"""
from zhon.hanzi import punctuation
from xpinyin import Pinyin
from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
import pandas as pd
import cv2
import numpy as np
from PIL import Image
from pyheatmap.heatmap import HeatMap
import matplotlib.pyplot as plt

 
#读取pdf文件
def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    lines = str(content).split("\n")
    units = [1, 2, 3, 5, 7, 8, 9, 11, 12, 13]
    header = '\x0cUNIT '
    # print(lines[0:10])
    count = 0
    flag = False
    return lines

#读取文本并返回无空格的字符串
def getstring():
    #获取文本
    my_pdf = open(filename, "rb")
    origin_list = read_pdf(my_pdf)
    my_pdf.close()
    #将文本列表转换为字符串
    origin_string = ''.join(origin_list)
    str = origin_string
    str = str.replace(" ","")
    #去除标点和数字
    punctuation_str = punctuation
    digits = ['0','1','2','3','4','5','6','7','8','9','．','(',')','-',',']
    for i in digits:
        str = str.replace(i,'')
    for i in punctuation:
        str = str.replace(i, ' ')
        str = str.replace('','')
    #去除空格
    new_string = str.replace(" ", "")
    #将结果字符串写入txt
    #txt = open("共产党宣言1_去除标点.txt", "w").write(str)
    #txt = open("共产党宣言2_去除空格.txt", "w").write(new_string)
    return new_string

#获取拼音
def getfreq():
    hanzi = getstring()
    p = Pinyin()
    result1 = p.get_pinyin(hanzi)
    str = result1
    #只保留字母
    str = str.replace('-', ' ')
    #将拼音转换结果写入txt
    txt = open("../output\\1_共产党宣言_拼音.txt", "w").write(str)
    #转换为列表
    list = str.split(" ")
    #转换为字典，以统计频率
    dict={}
    for key in list:
        dict[key]=dict.get(key,0)+1
    #排序后的拼音频率
    freq = (sorted(dict.items(), key = lambda kv:(kv[1], kv[0]),reverse=True))
    return str

#读取背景图片并绘制热力图
def apply_heatmap(image,data):
    #读取图片
    image1=cv2.imread(image)
    background = Image.new("RGB", (image1.shape[1], image1.shape[0]), color=0)
    #开始绘制热度图
    hm = HeatMap(data)
    hit_img = hm.heatmap(base=background, r = 135) # background为背景图片，r是半径，默认为10
    hit_img = cv2.cvtColor(np.asarray(hit_img),cv2.COLOR_RGB2BGR)#Image格式转换成cv2格式
    overlay = image1.copy()
    alpha = 0.5 # 设置覆盖图片的透明度
    cv2.rectangle(overlay, (0, 0), (image1.shape[1], image1.shape[0]), (255, 0, 0), -1) # 设置蓝色为热度图基本色蓝色
    image2 = cv2.addWeighted(overlay, alpha, image1, 1-alpha, 0) # 将背景热度图覆盖到原图
    image3 = cv2.addWeighted(hit_img, alpha, image2, 1-alpha, 0) # 将热度图覆盖到原图
    #cv2.imshow('ru',image3)
    #保存图片
    cv2.imwrite('../output\\1_heatmap.jpg',image3)
    cv2.waitKey(0)
    return image3

#读取图片分辨率
def readimage(image):
    image1=cv2.imread(image)
    sp = image1.shape
    height = sp[0] # height(rows) of image
    width = sp[1] # width(colums) of image
    chanael = sp[2] # the pixels value is made up of three primary colors
    print ( 'width: %d \nheight: %d \nnumber: %d' % (width, height, chanael))

#导入26个字母
def processLine(line, CharacterCounts):
    for character in line:
        if ord(character) in range(97, 123):
            CharacterCounts[character] += 1
  
#创建字母字典
def createCharacterCounts(CharacterCounts):
    for i in range(97, 123):
        CharacterCounts[chr(i)] = 0
        
#获取各字母出现频率(次数)  
def getletterfreq():
    zimu = []
    shuzi = []
    #filename = "共产党宣言3_拼音.txt"
    #infile = open(filename, "r")
    infile = str(getfreq())
    #建立用于计算词频的空字典
    CharacterCounts = {}
    #初始化字典键值
    createCharacterCounts(CharacterCounts)
    for line in infile:
        #liste.append(line)
        processLine(line.lower(), CharacterCounts)
    #从字典中获取数据对
    pairs = list(CharacterCounts.items())
    #列表中的数据对交换位置,数据对排序
    items = [[x,y] for (y,x) in pairs] 
    items.sort(reverse=True)
    for i in range(len(items)):
        zimu.append(items[i][1])
        shuzi.append(items[i][0])
    dicty = dict(zip(zimu,shuzi))
    return dicty

#绘制字母频率(次数)柱状图并保存
def pltbarchart():
    items = getletterfreq()
    zimu = list(items.keys())
    shuzi = list(items.values())
    letterfreq = dict(zip(zimu,shuzi))
    txt = open("../output\\1_字母按键频率.txt", "w").write(str(letterfreq))
    #绘制柱状图
    plt.figure(figsize=(14, 7)) 
    plt.bar(zimu,shuzi)
    for x,y in enumerate(shuzi):
        plt.text(x,y+100,'%s' %y,ha = 'center', va = 'bottom')
    #plt.bar(range(len(shuzi)), shuzi,tick_label=zimu)
    plt.title('letters freq bar chart')
    plt.xlabel('letter')
    plt.ylabel('freqency(times)')
    #保存柱状图
    plt.savefig('../output\\1_letter_freq_bar.jpg')
    #plt.show()
    zongshu = sum(shuzi)

def _main():
    getfreq()
    dicty = getletterfreq()
    addedlist = {a:[b[0],b[1],dicty[a]] for a, b in key_weights.items()}
    liste = addedlist.values()
    apply_heatmap('../data\\keyboard.jpg',(list(liste)))
    pltbarchart()
 
if __name__ == '__main__':
    filename = '../data\\共产党宣言.pdf'
    #键盘上各字母按键坐标
    key_weights = {
        'z':[250,380],'x':[340,380],'c':[430,380],'v':[520,380],'b':[610,380],'n':[700,380],'m':[790,380] ,
        'a':[210,290],'s':[300,290],'d':[390,290],'f':[480,290],'g':[570,290],'h':[680,290],'j':[770,290],'k':[860,290],'l':[950,290] ,
        'q':[180,200],'w':[270,200],'e':[360,200],'r':[450,200],'t':[540,200],'y':[630,200],'u':[720,200],'i':[810,200],'o':[900,200],'p':[990,200]
        }
    _main()
