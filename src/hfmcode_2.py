"""
2021/7/22
@author: 张新宇
生成二十六元哈夫曼树及其相应哈夫曼编码，得到最高效率对应总字符数
保存哈夫曼编码表(2_1_哈夫曼编码表.txt)、编码结果(2_2_编码结果.txt)以及解码结果(2_3_解码结果.txt)
"""
import math 
import xlwt
import random

#----------------------------------------生成哈弗曼树以及哈夫曼编码----------------------------------   
#树节点类的定义
class treenode:
    def __init__(self,key,freq):
        self.key = key #节点的名字
        self.freq = freq   #节点的概率
        #改后的child
        self.child = []
        for i in range(num1):
            self.child.append(None)
        self.code = '' #节点的编码


#创建树节点队列函数       
def create_noteQ(p_dict):
    Q=[]
    for i in p_dict.keys():
        Q.append(treenode(i,p_dict[i]))        
    Q.sort(key=lambda item:item.freq,reverse = True)#用lambda隐函数实现队列按照字母的概率降序排列
    return Q

#向队列中添加节点，并保证按照概率降序排序
def addQ(Q, nodeNew):
  if len(Q) == 0:
    return [nodeNew]
  else:
      Q=Q+[nodeNew]
      Q.sort(key=lambda item:item.freq,reverse=True)
      #每次加入节点都需要重新排列成降序
  return Q

#队列类的定义，该类有两个功能函数，当然本身有一个创建初始化的函数。另两个分别是添加节点和弹出最低概率节点。       
class Nodequeue:
    def __init__(self,p_dict):
        self.que = create_noteQ(p_dict)
        self.size = len(self.que)
        
    def addnode(self,node):
        self.que = addQ(self.que, node)
        self.size += 1
       
    def popNode(self):
        self.size -= 1
        return self.que.pop()
    #加入队列长度要+1，弹出长度-1
    
#创建huffman树，最后返回的是树的根节点        
def creatHuffmanTree(nodeQ,exact_division,exact_remainder):#第一个参数是队列，第二个参数就是是否能整除，第三个参数是余数(涉及第一次取的个数)
  if exact_division == True:
      node = ["" for i in range(num2)]
      for i in range(num2):
          node[i] = nodeQ.popNode()
      nodee = ''
      for i in range(num2):
          nodee = nodee + '+node[i].freq'
      r = treenode(None,eval(nodee))
      for i in range(num2):
          r.child[i] = node[num2-1-i]
      nodeQ.addnode(r)

  if exact_remainder == True:
      node = ["" for i in range(remainder)]
      for i in range(remainder):
          node[i] = nodeQ.popNode()
      nodee = ''
      for i in range(remainder):
          nodee = nodee + '+node[i].freq'
      r = treenode(None,eval(nodee))
      #r.leftchild = node2
      #r.midchild = node1
      for i in range(remainder):
          r.child[i] = node[remainder-1-i]
      nodeQ.addnode(r)

      
  while nodeQ.size != 1:
    node = ["" for i in range(num1)]  
    for i in range(num1):
        node[i] = nodeQ.popNode()

    nodee = ''
    for i in range(num1):
        nodee = nodee + '+node[i].freq'
    r = treenode(None, eval(nodee))#这里节点的名字是None表示是一个虚点，是由其他的点生成的一个节点，最后形成编码字典的时候会跳过虚点
    #r.leftchild = node3
    #r.midchild = node2
    #r.rightchild = node1

    for i in range(num1):
        r.child[i] = node [num1-1-i]
        
    nodeQ.addnode(r)
  return nodeQ.popNode()
  #最后返回的是队列的最后一个节点，也就是概率最大的点，就是这个huffman树的根节点

# 由哈夫曼树得到哈夫曼编码表,中序遍历，逢层赋值
def HuffmanCodeDic(roof, x):
  global codeDic, codeList
  if roof:#只要根不为空  
    roof.code += x
    if roof.key:
      codeDic2[roof.code] = roof.key
      codeDic1[roof.key] = roof.code
    #导入26个英文字母
    key_weights = {
            'j':1,'f':1,'k':1,'d':1,'l':0.9,'s':0.9,'a':0.8,
            'g':0.7,'h':0.7,'v':0.7,'i':0.7,'n':0.7,'t':0.6,'u':0.6,'e':0.6,'r':0.6,
            'b':0.5,'z':0.5,'x':0.5,'c':0.5,'m':0.5,'q':0.5,'w':0.5,'y':0.5,'o':0.5,'p':0.5
                }
    appendlist =  list(key_weights.keys())
    for i in range(num1):
        HuffmanCodeDic(roof.child[i], x+ appendlist[i])

# 字符串编码
def TransEncode(wordlist):
  global codeDic1
  transcode = ""
  for i in wordlist:
    transcode += codeDic1[i]
  return transcode

# 字符串解码
def TransDecode(StringCode):
  global codeDic2
  code = ""
  ans = ""
  for ch in StringCode:
    code += ch
    if code in codeDic2:
      ans += codeDic2[code]
      ans +=" "  
      code = ""
  return ans


#----------------------------------------生成哈弗曼树以及哈夫曼编码----------------------------------

def getkey_bal(filename):
    #各个字母所处键位均衡指数(人为定义)
    key_weights = {
    'j':1,'f':1,'k':1,'d':1,'l':0.9,'s':0.9,'a':0.8,
    'g':0.7,'h':0.7,'v':0.7,'i':0.7,'n':0.7,'t':0.6,'u':0.6,'e':0.6,'r':0.6,
    'b':0.5,'z':0.5,'x':0.5,'c':0.5,'m':0.5,'q':0.5,'w':0.5,'y':0.5,'o':0.5,'p':0.5
    }
    with open(filename, encoding='utf8') as f:
        wordlist = eval(f.read())
        letterfreq = dict(wordlist)

    
    liste_value = list(dict(letterfreq).values())
    all_value = sum(liste_value)
    value = []
    for i in liste_value:
        i = i/all_value
        i = round(i,4) #保留四位小数
        value.append(i) #各个字母频率百分数
    #print(value)
    keyliste = dict(letterfreq).keys()
    key_freqs = dict(zip(keyliste,value))
    key_bal = {a:round(b*key_weights[a],4) for a, b in key_freqs.items()}
    nm_key_bal = list(key_bal.values())
    sum_key_bal = round(sum(nm_key_bal),4)
    return sum_key_bal


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
def getletterfreq(stri):
    letterr = []
    numm = []
    #filename = "共产党宣言3_拼音.txt"
    #infile = open(filename, "r")
    infile = str(stri)
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
        letterr.append(items[i][1])
        numm.append(items[i][0])
    dicty = dict(zip(letterr,numm))
    return dicty

def getkey_bal2():
    #各个字母所处键位均衡指数(人为定义)
    key_weights = {
    'j':1,'f':1,'k':1,'d':1,'l':0.9,'s':0.9,'a':0.8,
    'g':0.7,'h':0.7,'v':0.7,'i':0.7,'n':0.7,'t':0.6,'u':0.6,'e':0.6,'r':0.6,
    'b':0.5,'z':0.5,'x':0.5,'c':0.5,'m':0.5,'q':0.5,'w':0.5,'y':0.5,'o':0.5,'p':0.5
    }
    #with open(filename, encoding='utf8') as f:
    #    wordlist = eval(f.read())
    #    letterfreq = dict(wordlist)
    letterfreq = getletterfreq(a)
    
    liste_value = list(dict(letterfreq).values())
    all_value = sum(liste_value)
    value = []
    for i in liste_value:
        i = i/all_value
        i = round(i,4) #保留四位小数
        value.append(i) #各个字母频率百分数
    #print(value)
    keyliste = dict(letterfreq).keys()
    key_freqs = dict(zip(keyliste,value))
    key_bal = {a:round(b*key_weights[a],4) for a, b in key_freqs.items()}
    nm_key_bal = list(key_bal.values())
    sum_key_bal = round(sum(nm_key_bal),4)
    return sum_key_bal

if __name__ == '__main__':
    #哈夫曼树元数(26个字母对应26元)
    num1=26
    num2=num1-1
    filename = '1_字母按键频率.txt'

    #中文拼音(全拼)出现的频率(次数)
    p_dict={}#这个字典用来存信源字母及其频率
    with open('1_共产党宣言_拼音.txt', encoding='utf8') as f:
        wordlist = f.read().split(' ')     # .read()获得所有内容； .split(' ')按' '分割成列表
        string = ''.join(wordlist)
    worddict = {}
    for key in wordlist:
        worddict[key] = worddict.get(key,0) + 1
    liste = sorted(worddict.items(), key = lambda kv:(kv[1], kv[0]),reverse= True)
    p_dict = dict(liste)#字典格式{字母1：概率，字母2：概率....}

    #判断余数，确定第一次取的个数
    #判断余数为多维哈夫曼树的要点，若能被num2整除，则第一次取num2个，若余1，则第一次取num1个，其余情况余数为多少，就取多少个。
    remainder = len(p_dict.keys()) % (num2)
    if remainder == 0:
        exact_division = True
        exact_remainder = False
    elif remainder == 1:
        exact_division = False
        exact_remainder = False
    else:
        exact_remainder = True
        exact_division = False

    #由树得到哈夫曼编码表
    codeDic1 = {}#编码字典
    codeDic2 = {}#解码字典
    t = Nodequeue(p_dict)
    tree = creatHuffmanTree(t,exact_division,exact_remainder)
    HuffmanCodeDic(tree, '')

    #将哈夫曼编码与原全拼方案音节、频率对应
    addlist1 = dict(liste)
    addlist2 = dict(codeDic1)
    addedlist = {a:[b,addlist2[a]] for a, b in addlist1.items()}
    keyslist = addedlist.keys()
    valuelist = addedlist.values()
    keys = []
    times = []
    hfmcode = []
    for i in valuelist:
        times.append(i[0])
        hfmcode.append(i[1])
    for i in keyslist:
        keys.append(i)

    originlen = 0   #全拼编码方案总字符长度
    hfmlen = 0      #哈夫曼编码方案总字符长度(最高效率情况)
    leng = len(keys)
    for i in range(leng):
        originlen = originlen + len(keys[i])*times[i]
        hfmlen = hfmlen + len(hfmcode[i])*times[i]
        
    #result = str(addedlist)
    #result += '\n\n' + '格式为 \'全拼编码\':[出现次数,\'哈夫曼编码\']'
    #result += '\n'+ '原全拼编码方案总字符长度:' + ' %s' %originlen + '哈夫曼编码方案总字符长度:' + ' %s' %hfmlen +'全拼编码方案的输入效率为%s' %qp_xl

    #哈夫曼编码表
    #txt = open("2_哈夫曼编码表.txt", "w").write(str(codeDic1))
    #txt = open("2_1_哈夫曼编码表.txt", "w").write(result)
    #编码结果
    a = TransEncode(wordlist)
    #txt = open("2_2_编码结果.txt", "w").write(a)
    #解码结果
    aa = TransDecode(a)
    #txt = open("2_3_解码结果.txt", "w").write(aa)

    hfmcode_str = ''
    for i in addedlist:
        hfmcode_str += i + ': ' + str(addedlist[i]) + '\n'
    

    #全拼编码方案的均衡性
    qp_jhx = getkey_bal(filename)
    #哈夫曼编码方案的均衡性
    hfm_jhx = getkey_bal2()
    #全拼编码方案的输入效率
    qp_xl = round(hfmlen / originlen , 4)
    
    #效率的定义文本
    str_xl = '输入效率定义为当前编码方式输入总字符数与哈夫曼编码输入总字符数的比值，采用哈夫曼编码时的输入总字符数对应最高效率情况。\n'
    #str_xl += str(addedlist) #\n哈夫曼编码结果如下（格式为 \'全拼编码\':[出现次数,\'哈夫曼编码\']）：
    str_xl += '原全拼编码方案总字符长度:' + ' %s\n' %originlen + '哈夫曼编码方案总字符长度:' + ' %s\n' %hfmlen +'全拼编码方案的输入效率为: %s\n' %qp_xl
    #均衡性的定义文本
    str_jhx = '\n均衡性可定义为每个字母按键所使用的次数；也可定义为手指在键盘上按照手指放置区域与按下字母按键位置所需移动的距离，在输入时手指所需移动的距离越小，越均衡。这里我们选择后者作为均衡性的定义。\n'
    str_jhx +='按照手指放置位置，将26个字母按键分别人为设定各自的\"均衡指数\"，再将各个字母按键的使用频率(归一化)与其均衡指数相乘，将结果累加后，得到总的均衡指数，可以表征均衡性。\n'
    str_jhx +='根据均衡性的定义，我们可以知道：总均衡指数越接近于1，均衡性约好，越接近于0，均衡性越差。\n'
    str_jhx +='使用全拼编码方案时的总均衡指数为: %s' %qp_jhx
    
    txt = open("2_输入效率与均衡性.txt", "w").write(str_xl+str_jhx)

    str_hfmcode = '采用哈夫曼树进行编码，得到的新编码方式在附录1中（格式为 \'全拼编码\':[出现次数,\'哈夫曼编码\']）\n'
    str_hfmcode += '新的编码方式总字符长度为 %s,对应最高效率1.\n' %hfmlen
    str_hfmcode += '新的编码方式总均衡指数为 %s, ' %hfm_jhx
    str_hfmcode += '高于全拼编码方案的总均衡指数%s \n' %qp_jhx
    str_appendix1 = '附件1: 哈夫曼编码表（格式为 \'全拼编码\':[出现次数,\'哈夫曼编码\']）\n'+hfmcode_str
    str_appendix2 = '附件2: 编码结果\n' +a
    str_appendix3 = '附件3: 解码结果\n' +aa

    txt = open("3_新的编码方式.txt", "w").write(str_hfmcode)
    txt = open("附件1_哈夫曼编码表.txt", "w").write(str_appendix1)
    txt = open("附件2_编码结果.txt", "w").write(str_appendix2)
    txt = open("附件3_解码结果.txt", "w").write(str_appendix3)
