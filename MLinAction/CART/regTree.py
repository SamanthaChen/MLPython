#coding=utf-8
from numpy import *

#加载数据
def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine) #map all elements to float() 将每行映射成浮点
        dataMat.append(fltLine)
    return dataMat

#二分切割数据集
def binSplitDataSet(dataSet, feature, value):
    mat0=dataSet[nonzero()]