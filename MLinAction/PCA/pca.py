#coding=utf-8
'''
2016.9.18 samanthachen
'''
'''
减去平均数
计算协方差矩阵
计算协方差矩阵的特征值和特征向量
将特征值从大到小排序
保留最大的K个特征向量
将数据转换到上述K各特征向量构建的新空间中
'''
from numpy import *

#加载数据
def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float,line) for line in stringArr]
    return mat(datArr)

def pca(dataMat, topNfeat=9999999):
    #计算并减去原始数据的平均值
    meanVals=mean(dataMat,axis=0)
    meanRemoved=dataMat-meanVals
    #计算矩阵的协方差矩阵
    covMat=cov(meanRemoved,rowvar=0)
    #计算特征向量，特征值
    eigVals,eigVects=linalg.eig(mat(covMat))
    #特征值从小到大排序
    eigValInd=argsort(eigVals)
    eigValInd=eigValInd[:-(topNfeat+1):-1]
    redEigVects=eigVects[:,eigValInd] #按特征值大到小排序的特征向量 W
    #将原数据转移到新的空间
    lowDDataMat=meanRemoved*redEigVects #cov(X)*W 投影到特征空间
    reconMat=(lowDDataMat*redEigVects.T)+meanVals #  cov(X)*W*WT+mean 重构数据
    return lowDDataMat,reconMat #

#main
#main
if __name__=='__main__':
    dataMat=loadDataSet('testSet.txt')
    lowData,reconMat=pca(dataMat,2)
    #画图
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(dataMat[:,0].flatten().A[0], dataMat[:,1].flatten().A[0], marker='^',s=90) #原来的数据
    ax.scatter(reconMat[:,0].flatten().A[0], reconMat[:,1].flatten().A[0], marker='o',s=50,c='red') #重构的数据
    plt.show()
