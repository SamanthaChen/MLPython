#coding=utf-8
from numpy import *



#加载数据
def loadDataSet(fileName):      #general function to parse tab -delimited floats
    '''
    根据外存文件加载数据，返回矩阵
    :param fileName:
    :return:
    '''
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine) #map all elements to float() 将每行映射成浮点
        dataMat.append(fltLine)
    return dataMat

#二分切割数据集
def binSplitDataSet(dataSet, feature, value):
    '''
    将dataset按照特征和特征值进行切分
    :param dataSet:
    :param feature:
    :param value:
    :return:
    '''
    mat0=dataSet[nonzero(dat<=value)[0],:][0]
    return mat0,mat1

def createTree(dataSet,leafType=regLeaf, errType=regErr, ops=(1,4)):
    '''

    :param dataSet:
    :param leafType: 建立叶节点的函数aSet[:,feature]>value)[0],:][0]
    mat1=dataSet[nonzero(dataSet[:,feature]
    :param errType: 误差计算函数
    :param ops:
    :return:
    '''
    feat,val=chooseBest
