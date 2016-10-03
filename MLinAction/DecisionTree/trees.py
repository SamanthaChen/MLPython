#coding=utf-8
from math import log
import operator

#计算给定数据集的香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts={}
    #为所有可能的类创建字典
    for featVec in dataSet:
        currentLabel  =featVec[-1] #最后一行是标签
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel] += 1
    shannonEnt=0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob*log(prob,2)
    return  shannonEnt

#简单的鉴定数据集
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

# 按照给定的特征划分数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
             #抽取出来的数据不包含axis这个特征
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# 选择最好的数据集划分方式
#这里用的是信息增益
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
            subDatsSet = splitDataSet(dataSet,i,value) #选择第i个特征的value特征进行划分
            prob = len(subDatsSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDatsSet)
        infoGain=baseEntropy-newEntropy
        #更新当前最好的信息熵
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

# 多数表决方式
def majorityCnt(classList):
    classCount = {}
    for vote in classCount:
        if vote not in classCount.keys(): classCount[vote]=0
        classCount[vote] += 1
    #按照频率降序排列
    sortedClassCount = sorted(classCount.iteritems(),\
                              key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0] #返回出现次数最多的类名

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
    #del(labels[bestFeat]) #获得除去当前最好的划分特征后的特征列表
    featValue = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValue)
    for value in uniqueVals:
        subLabels=labels[:]#深拷贝，防止修改原对象
        del(subLabels[bestFeat]) #获得除去当前最好的划分特征后的特征列表
        myTree[bestFeatLabel][value]=creatTree(splitDataSet(dataSet,bestFeat,value),subLabels) #递归的创建树

    return myTree

def classify(inputTree,featLabels,testVec):
    '''
    分类
    :param inputTree:
    :param featLabels:
    :param testVec:
    :return:
    '''
    firstStr = inputTree.keys()[0]
    # print firstStr
    secondDict = inputTree[firstStr]
    # print featLabels
    featIndex = featLabels.index(firstStr)
    # print featIndex
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel

#####使用pickle存储决策树
def storeTree(inputTree,fileName):
    import pickle
    fw=open(fileName,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(fileName):
    import pickle
    fr=open(fileName)
    return pickle.load(fr)

if __name__=='__main__':
    # myDat,labels=createDataSet()
    # # print labels
    # myTree=creatTree(myDat,labels)
    # print classify(myTree,labels,[1,1])

    #建树并且序列化
    # fr=open('lenses.txt')
    # lenses=[inst.strip().split('\t') for inst in fr.readlines()]
    # lensesLabels=['age','prescript','astigmatic','tearRate']
    # lensesTree=creatTree(lenses,lensesLabels)
    # storeTree(lensesTree,'lensesTree.txt')

    #反序列化树
    tree=grabTree('lensesTree.txt')
    lensesLabels=['age','prescript','astigmatic','tearRate']
    print classify(tree,lensesLabels,['presbyopic	hyper','yes','normal'])