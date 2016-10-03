#coding=utf-8
from numpy import *
def loadDataSet():
    dataMat=[]
    labelMat=[]
    fr=open('testSet.txt')
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmod(intX):
    return 1.0/(1+exp(-intX))

def gradAscent(dataMatInt, classLables):
    '''
    批量梯度更新
    :param dataMatInt:
    :param classLables:
    :return:
    '''
    dataMatrix=mat(dataMatInt)
    labelMat=mat(classLables).transpose()
    m,n=shape(dataMatrix)
    alpha=0.001
    maxCycles=500
    weidghts=ones((n,1))
    for k in range(maxCycles):
        #这里是矩阵相乘，是所有的样本
        h=sigmod(dataMatrix*weidghts)
        error=(labelMat-h)
        weidghts=weidghts+alpha*dataMatrix.transpose()*error
    return weidghts

def stocGradAscent0(dataMatrix, classLabels):
    '''
    随机梯度：alpha固定，每次随机选择一个样本
    :param dataMatrix:
    :param classLabels:
    :return:
    '''
    m,n=shape(dataMatrix)
    alpha=0.01
    weights=ones(n)
    for i in range(m):
        #这里是一个一个的array计算
        h=sigmod(sum(dataMatrix[i]*weights))
        error=classLabels[i]-h
        weights =weights+alpha*error*dataMatrix[i]
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    '''
    随机梯度下降：
    :param dataMatrix:
    :param classLabels:
    :param numIter:
    :return:
    '''
    m,n=shape(dataMatrix)
    weights=ones(n)
    for j in range(numIter):
        dataIndex=range(m)
        for i in range(m):
            alpha=4/(1.0+j+i)+0.01
            randIndex=int(random.uniform(0,len(dataIndex)))
            h=sigmod(sum(dataMatrix[randIndex]*weights))
            error=classLabels[randIndex]-h
            weights=weights+alpha*error*dataMatrix[randIndex]
            del(dataIndex[randIndex]) #更新完一个样本就删掉这个样本的编号
    return weights


if __name__=='__main__':
    dataArr,labelMat=loadDataSet()
    w1= gradAscent(dataArr,labelMat) # 批量梯度更新
    print w1
    w2=stocGradAscent0(array(dataArr),labelMat)
    print w2
    w3=stocGradAscent1(array(dataArr),labelMat)
    print w3
    #
    # plotBestFit(w1.getA())
    # plotBestFit(w2)
    # multiTest()