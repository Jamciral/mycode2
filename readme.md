# 基于哈夫曼树的全拼编码改进




# 目录
1.  * [题目介绍](#题目介绍)
2.  * [项目摘要](#项目摘要)
3.  * [必要条件](#必要条件)
4.  * [用法](#用法)
5.  * [结果](#结果)



## 题目介绍

题目：高效均匀的打字编码方法

由于不同汉字的使用频率和输入方式不同，使用全拼输入法撰写文章时，26个字母键盘的使用频率并不均衡。

假设给定一篇中文文章素材（附件文章），使用全拼输入法（不考虑词组缩写）输入这篇文章中的文字。

请你评价使用全拼时26字母按键的均衡性和输入效率，并尝试设计一种新的拼写编码方法，使得输入同样文章时按键使用更加均衡、输入更加高效。

  

具体要求：  

1. 给定一篇中文文章（附件中的文章），统计出使用全拼输入法录入这篇文章时26个字母键的使用频率，绘制热力图。  

 &#8195 - 输入: 一篇中文文章（附件文章）  

- 输出: 录入这篇文章的26字母键使用热力图  

  

2. 设计评价标准来分别评价使用全拼录入这篇文章时的按键使用均衡性和输入效率（请根据个人理解自行定义，建议使用明确的量化指标）。  

- 输出: 量化评价标准或方法，以及对全拼输入方案的评价结果  

  

3. 基于你在题目2中制定的标准，尝试在全拼基础上改进打字编码方案，使得输入该文章时字母键的使用更加均衡、输入更加高效，展示改进的结果并分析。  

- 输入: 一篇中文文章（附件文章）  

- 输出: 新的打字编码方案、新旧方案在均衡性和输入效率方面的对比

## 项目摘要

本项目主要实现了三个部分功能。<br>
1.根据输入的中文文本统计出全拼方案拼音出现频率(次数)、字母出现次数并绘制出字母热力图。<br>
2.利用哈夫曼树原理，通过构建二十六叉哈夫曼树得到二十六元的哈夫曼编码（基于26个字母），得到了输入该文本所需的最短字符数。<br>
3.定义最高输入效率以及总平衡指数，优化得出新的编码方式。<br>

## 必要条件

本项目需要用到python(2.7及以上版本)，需要运行以下库：
>     from zhon.hanzi import punctuation
>     from xpinyin import Pinyin
>     from io import StringIO
>     from io import open
>     from pdfminer.converter import TextConverter
>     from pdfminer.layout import LAParams
>     from pdfminer.pdfinterp import PDFResourceManager, process_pdf
>     import pandas as pd
>     import cv2
>     import numpy as np
>     from PIL import Image
>     from pyheatmap.heatmap import HeatMap
>     import matplotlib.pyplot as plt
>     import math 
>     import xlwt
>     import random


## 用法

输入指令:
>     python3 src/main.py

## 结果

共生成9个文件：

- [1_heatmap.jpg](https://github.com/Jamciral/mycode2/blob/master/output/1_heatmap.jpg) : 全拼编码方案下输入文章时的键盘热力图（***第一问结果***）
- 1_letter_freq_bar.jpg : 全拼编码方案下输入完整文本时的字母按键频率柱状图
- 1_共产党宣言_拼音.txt : 将中文转换为全拼编码方案
- 1_字母按键频率.txt : 全拼编码方案下输入完整文本时的字母按键频率
- [2_输入效率与均衡性.txt](https://github.com/Jamciral/mycode2/blob/master/output/2_%E8%BE%93%E5%85%A5%E6%95%88%E7%8E%87%E4%B8%8E%E5%9D%87%E8%A1%A1%E6%80%A7.txt) : 全拼编码方案的输入效率与均衡性评价(***第二问结果***)
- [3_新的编码方式.txt](https://github.com/Jamciral/mycode2/blob/master/output/3_%E6%96%B0%E7%9A%84%E7%BC%96%E7%A0%81%E6%96%B9%E5%BC%8F.txt) : 哈夫曼编码方式的输入效率与均衡性评价(***第三问结果***)
- 附件1_哈夫曼编码表.txt
- 附件2_编码结果.txt
- 附件3_解码结果.txt


