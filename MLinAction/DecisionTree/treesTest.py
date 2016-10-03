#coding=utf-8
from math import log
import operator

def calcShannonEnt(dataSet):
    '''
    计算信息熵
    :param dataSet:
    :return:
    '''
    numEntries=len(dataSet)
    labelCounts={}
    for featureVec in dataSet:
        currentLabel=featureVec[-1] #最后一个是标签
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel] += 1

    ShannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        ShannonEnt -= prob*log(prob,2)
    return ShannonEnt

def createDataSet():
    '''
    简单的数据集
    :return:
    '''
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

def splitDataset(dataSet, axis, value):
    '''
    将数据集按照axis和value进行划分
    :param dataSet:
    :param axis:
    :param value:
    :return:
    '''
    retDataSet=[]
    for featVec in dataSet:
        if featVec in dataSet:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet) #基本的特征的熵H(D)
    bestInfoGain = 0.0;
    bestFeature = -1;
    for i in range(numFeatures):
        #抽取特征，创建唯一的分类标签列表
        featureList = [example[i] for example in dataSet]
        uniqueVals = set(featureList)
        #计算每种划分方式的信息熵
        newEntropy=0.0
        for value in uniqueVals:
            subDatsSet = splitDataset(dataSet,i,value) #选择第i个特征的value特征进行划分
            prob = len(subDatsSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDatsSet)
        infoGain=baseEntropy-newEntropy
        #更新当前最好的信息熵
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

def majorityCnt(classList):
    '''
    多数表决，返回最大的类
    :param classList:
    :return:
    '''
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
        sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
        return sortedClassCount[0][0]


# 创建树的函数代码
def creatTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    # 第一个停止条件：类别相同即停止划分
    if classList.count(classList[0])==len(classList):
        return classList[0]
    # 第二个条件：遍历完所有的特征，直接返回出现次数最多的
    if len(dataSet[0])==1:
        return majorityCnt(classList)

    # 获取最好的划分特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]

    myTree = {bestFeatLabel:{}}  #树的跟是最好的划分特征的标签
    del(labels[bestFeat]) #获得除去当前最好的划分特征后的特征列表
    featValue = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValue)
    for value in uniqueVals:
        subLabels=labels[:]#深拷贝，防止修改原对象
        myTree[bestFeatLabel][value]=creatTree(splitDataset(dataSet,bestFeat,value),subLabels) #递归的创建树

    return myTree

if __name__=='__main__':
    myDat,labels=createDataSet()
    print creatTree(myDat,labels)
