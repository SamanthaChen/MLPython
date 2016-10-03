#coding=utf-8
'''
Created on 2016.9.17

@author: Samathachen
'''

from numpy import *

#加载数据
def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) - 1 #get number of fields
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

# 利用矩阵的方法计算回归系数，标准线性回归
def standRegres(xArr, yArr):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0.0: #说明不存在逆
        print 'This matrix is singular, cannot do inverse'
        return
    ws=xTx.I * (xMat.T*yMat)
    return ws

#局部加权线性回归（LWLR）
#使用了一个RBF核来对附近的点赋予更高的权重
#给定一个点，计算出对应的预测值yhat,k是RBF核的参数
def lwlr(testPoint, xArr, yArr, k=1.0):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    m=shape(xMat)[0]
    weidghts = mat(eye((m))) #创建对角矩阵
    for j in range(m):
        diffMat=testPoint-xMat[j,:] #第j行，即第j个样本
        weidghts[j,j]=exp(diffMat*diffMat.T/(-2.0*k**2)) #权重大小按照距离进行衰减
    xTx=xMat.T *(weidghts*xMat)
    #测试能不能求逆
    if linalg.det(xTx)==0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws=xTx.I*(xMat.T*(weidghts*yMat))
    return testPoint*ws

#得到数据集里面所有点的估计
def lwlTest(testArr, xArr, yArr, k=1.0):
    m=shape(testArr)[0]
    yHat=zeros((m))
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr,k)
    return yHat

#岭回归
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    denom=xTx+eye(shape(xMat)[1])*lam
     #测试能不能求逆
    if linalg.det(denom)==0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws=denom.I*(xMat.T*yMat)
    return ws
#
def ridgeTest(xArr,yArr):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    #对数据进行标准化
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMean=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMean)/xVar
    #
    numTestPts=30
    wMat=zeros((numTestPts,shape(xMat)[1]))
    #每个点获得一个w
    for i in range(numTestPts):
        ws=ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat

#Lasso回归
def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    #数据标准化，满足0均值和单位方差
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMat=regularize(xMat)
    m,n=shape(xMat)
    returnMat=zeros((numIt,n)) #记录每一次迭代的w

    ws=zeros((n,1))
    wsTest=ws.copy()
    wsMax=ws.copy()

    for i in range(numIt):
        print ws.T
        lowestError=inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest[j]+=eps*sign
                yTest=xMat*wsTest
                rssE=rssError(yMat.A,yTest.A) #计算平方误差和
                if rssE<lowestError:
                    lowestError=rssE
                    wsMax=wsTest
        ws=wsMax.copy()
        returnMat[i,:]=ws.T
    return returnMat




def regularize(xMat):#regularize by columns
    '''
    对矩阵进行
    :param xMat:
    :return:
    '''
    inMat = xMat.copy()
    inMeans = mean(inMat,0)   #calc mean then subtract it off 计算均值
    inVar = var(inMat,0)      #calc variance of Xi then divide by it 计算方差
    inMat = (inMat - inMeans)/inVar #（x-均值）/方差
    return inMat

def rssError(yArr,yHatArr): #yArr and yHatArr both need to be arrays
    '''
    计算平方误差和
    :param yArr:
    :param yHatArr:
    :return:
    '''
    return ((yArr-yHatArr)**2).sum()

#main函数
if __name__=='__main__':
    #标准的二次回归
    # xArr,yArr=loadDataSet('ex0.txt')
    # print xArr,yArr
    # ws=standRegres(xArr,yArr) #求得回归系数
    # print ws
    #yHat=xCopy*ws #回归的直线

    #局部加权线性回归
    xArr,yArr=loadDataSet('ex0.txt')
    yHat=lwlTest(xArr,xArr,yArr,0.1)


    #画图
    xMat=mat(xArr)
    yMat=mat(yArr).T
    #对xArr排序
    srtInd=xMat[:,1].argsort(0)
    xSort=xMat[srtInd][:,0,:]

    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(xSort[:,1],yHat[srtInd])
    ax.scatter(xMat[:,1].flatten().A[0],yMat[:,0].flatten().A[0],s=2,c='red')
    plt.show()


