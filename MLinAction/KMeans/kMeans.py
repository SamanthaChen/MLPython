#coding=utf-8
'''
2016.9.17创建，有误还未修改完毕
'''
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

#计算两个向量的欧式距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA-vecB,2)))

#为给定数据集构建一个包含k个随机的质心的集合
def randCent(dataSet,k):
    n=shape(dataSet)[1]
    centroids=mat(zeros((k,n)))
    for j in range(n):
        minJ=min(dataSet[:,j])
        rangeJ=float(max(dataSet[:,j])-minJ)
        centroids[:,j]=minJ+random.rand(k,1)
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2))) #两维，第一维是索引，第二维是距离的平方
    centroids=createCent(dataSet,k)
    clusterChanged=True #收敛标志
    while clusterChanged:
        clusterChanged=False
        for i in range(m): #遍历所有样本
            minDist=inf
            minIndex=-1
            for j in range(k): #遍历所有中心
                distJI=distMeas(centroids[j:],dataSet[i,:])
                if distJI<minDist:
                    minDist=distJI
                    minIndex=j #记录最近的第j个中心点
                if clusterAssment[i,0]!=minIndex:
                    clusterChanged=True
                clusterAssment[i,:]=minIndex,minDist**2
        print centroids
        #更新质心的位置
        for cent in range(k):
            ptsInClust=dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:]=mean(ptsInClust,axis=0)
    return centroids,clusterAssment





if __name__=='__main__':
    dataMat=mat(loadDataSet('testSet.txt'))
    print kMeans(dataMat,4)