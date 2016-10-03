#coding=utf-8
from numpy import *
#产生训练数据
def loadDataSet():
    #该数据取自某狗狗论坛的留言版
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    #标注每条数据的分类，这里0表示正常言论，1表示侮辱性留言
    classVec = [0,1,0,1,0,1]
    return postingList,classVec

def createVocabList(dataSet):
    '''
    返回一个不重复词的列表
    :param dataSet:
    :return:
    '''
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet | set(document)  #创建两个集合的并集
    return list(vocabSet)

def setOfWord2Vec(vocabList, inputSet):
    '''
    词集模型，返回文档向量：表示词汇表中的单词在输入文档中是否出现
    :param vocabList:
    :param inputSet:
    :return:
    '''
    returnVec = [0]*len(vocabList) #创建一个其中所含的元素都是0的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:print "the word: %s is not in my Vocabulary" %word

    return returnVec

def trainNB0(trainMatrix, trainCategory):
    '''
    :param trainMatrix:输入的文档矩阵
    :param trainCategory:每篇文档类别标签所构成的向量
    :return:
    '''
    #留言数目
    numTrainDocs=len(trainMatrix)
    #变换矩阵的行列数目，即词汇表数目
    numWords=len(trainMatrix[0])
    #侮辱性留言的概率
    pAbusive=sum(trainCategory)/float(numTrainDocs) #类别为1
    p0Num=ones(numWords) #p(wi|c0) 初始化为1是为了防止出现0的情况
    p1Num=ones(numWords) #p(wi|c1)
    p0Denom=2.0
    p1Denom=2.0
    for i in range(numTrainDocs):
         #统计每类单词的数目，注意我们这里讨论的是一个二分问题
        #所以可以直接用一个if...else...即可，如果分类较多，则需要更改代码
        if trainCategory[i]==1:
            p1Num += trainMatrix[i] #每个词汇对应类别1出现的次数
            p1Denom += sum(trainMatrix[i]) #该文档总的词汇数
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    #用log是为了防止下溢出，求对数的话两个概率相乘可以直接变成两个概率的对数相加，就不会变成极小的数相乘的情况
    p1Vect=log(p1Num/p1Denom) #每个词汇对应类别1的概率
    p0Vect=log(p0Num/p0Denom) #每个词汇对应类别0的概率

    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0


def testingNB():
    '''
    #内嵌测试函数
    :return:
    '''
    listOPosts,listClasses=loadDataSet()  #加载文章和列别
    myVocabList=createVocabList(listOPosts)  #根据文章获得不重复的词汇表
    trainMat=[]  #训练矩阵
    #将文档中的词向量转换为训练矩阵
    for postinDoc in listOPosts:
      trainMat.append(setOfWord2Vec(myVocabList,postinDoc))
    #分别计算每个词在类别0和类别1下的条件概率
    p0V,p1V,p1=trainNB0(trainMat,listClasses)

    #测试数据1
    testEntry=['love','my','dalmation']
    #将测试数据变为词向量
    thisDoc=setOfWord2Vec(myVocabList,testEntry)
    #打印训练结果
    print testEntry,"classified as:",classifyNB(thisDoc,p0V,p1V,p1)

     #测试数据2
    testEntry=['garbage','stupid']
    thisDoc=setOfWord2Vec(myVocabList,testEntry)
    print testEntry,"classified as:",classifyNB(thisDoc,p0V,p1V,p1)

def bagOfWord2VecMN(vocabList, inputSet):
    '''
    词集模型，返回文档向量：表示词汇表中的单词在输入文档中是否出现
    :param vocabList:
    :param inputSet:
    :return:
    '''
    returnVec = [0]*len(vocabList) #创建一个其中所含的元素都是0的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def textParse(bigString):
    '''
    该函数将每个句子都解析成单词，并忽略空格，标点符号以及长度小于3的单词
    :param bigString:
    :return:
    '''
    import re
    listOfTokens=re.split(r'\w*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]

def spamTest():
    '''
    #检测垃圾邮件
    :return:
    '''
    docList=[]
    classList=[]
    fullText=[]
    #分别读取邮件内容
    for i in range(1,26):
        #垃圾邮件
        wordList=textParse(open('email/spam/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)

        #正常邮件
        wordList=textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    trainingSet=range(50)
    testSet=[]
    #随机抽取作为测试集
    for i in range(10):
        #从50个数据集中随机选取十个作为测试集，并把其从训练集中删除
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat=[]
    trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWord2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])

    #使用训练集得到概率向量
    p0V,p1V,pSpam=trainNB0(array(trainMat),array(trainClasses))
     #测试分类器的错误率
    errorCount=0
    for docIndex in testSet:
        wordVector=setOfWord2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
            print "Classification error:"
            print docList[docIndex]
    print errorCount
    print "the error rate is:",float(errorCount)/len(testSet)


def spamTest2():
    #存放输入数据
    docList=[]
    #存放类别标签
    classList=[]
    #所有的文本
    fullText=[]
    #分别读取邮件内容
    for i in range(1,26):
        wordList=textParse(open('email/spam/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    #range(50)表示从0到50，不包括50
    trainingSet=range(50)
    #测试集
    testSet=[]
    #随机抽取是个作为测试集
    for i in range(10):
        #从50个数据集中随机选取十个作为测试集，并把其从训练集中删除
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[];
    for docIndex in trainingSet:
        trainMat.append(setOfWord2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    #使用训练集得到概率向量
    p0V,p1V,pSpam=trainNB0(array(trainMat),array(trainClasses))
    #测试分类器的错误率
    errorCount=0
    for docIndex in testSet:
        wordVector=setOfWord2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
            print "Classification error:"
            print docList[docIndex]
    print errorCount
    print "the error rate is:",float(errorCount)/len(testSet)
    return float(errorCount)/len(testSet)


'''
4.7 使用朴素贝叶斯分类器从个人广告中获取区域倾向
'''
def calcMostFreq(vocabList,fullText):
    '''
    计算出现频率，
    :param vocabList:
    :param fullText:
    :return: 返回前30个
    '''
    import operator
    freqDict={}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq=sorted(freqDict.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:30]

def localWords(feed1,feed0):
    import feedparser
    docList=[]
    classList=[]
    fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    #每次访问一条rss源
    for i in range(minLen):
        #第1类
        wordList=textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        #第0类
        wordList=textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList) #建立词汇表
    #去掉出现次数最高的高频词
    top30Words=calcMostFreq(vocabList,fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])
    #构建训练集和测试集
    trainingSet=range(2*minLen)
    testSet=[]
    for i in range(20):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainingMat=[]
    trainClasses=[]
    for docIndex in trainingSet:
        trainingMat.append(bagOfWord2VecMN(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    #训练贝叶斯模型
    p0V,p1V,pSpam=trainNB0(array(trainingMat),array(trainClasses))
    erroCount=0
    for docIndex in testSet:
        wordVec=bagOfWord2VecMN(vocabList,docList[docIndex])
        if classifyNB(array(wordVec),p0V,p1V,pSpam)!=classList[docIndex]:
            erroCount += 1
    print 'the error rate is:',float(erroCount)/len(testSet)
    return vocabList,p0V,p1V



if __name__=='__main__':
    # testingNB()
    # rate=0.0
    # for i in range(1,21):
    #     r=spamTest2()
    #     rate+=r
    # print '平均错误率：%.4f' %(rate/20)

    #RSS
    import feedparser
    ny=feedparser.parse('http://newyork.craiglist.org/stp/index.rss')
    sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    vocabList,pSF,pNY=localWords(ny,sf)
    vocabList,pSF,pNY=localWords(ny,sf)
