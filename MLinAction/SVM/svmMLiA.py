#coding=utf-8
import random
from numpy import *

#加载数据
def loadDataSet(fileName):
    dataMat=[]
    labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

#用于0到m之间随机选一个数，但是不能等于i
def selectJrand(i,m):
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return j

#调整alpha位于L和H之间
def clipAlpha(aj, H, L):
    if aj>H:
        aj=H
    if L>aj:
        aj=L
    return aj

# 简单的SMO算法
#@param 数据集，类别标签，常数C，容错率和退出的最大循环次数
def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    #将数组装换为矩阵
    dataMatrix=mat(dataMatIn)
    labelMat=mat(classLabels).transpose()
    b=0
    m,n=shape(dataMatrix)
    alphas = mat(zeros((m,1))) #m*1的零向量
    iter=0
    while (iter<maxIter):
        alphaPairsChanged=0 #用于记录alpha是否已经被优化
        for i in range(m):
            #fXi是我们预测的类别 g(x) = sum(alphas*Y*K(xi,x))+b
            fXi=float(multiply(alphas,labelMat).T * (dataMatrix*dataMatrix[i,:].T))+b
            #Ei是误差
            Ei=fXi-float(labelMat[i])
            #测试误差是否可以接受，如果误差很大，就需要进行调整
            if((labelMat[i]*Ei <-toler and alphas[i]<C) or (labelMat[i]*Ei>toler and alphas[i]>0) ):
                j=selectJrand(i,m) #随机选择另一个aplpha变量进行调整
                #计算误差
                fXj=float(multiply(alphas,labelMat).T * (dataMatrix*dataMatrix[j,:].T))+b
                Ej=fXj-float(labelMat[j])
                #复制alpha老值
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                #求解两个变量的二次规划问题
                if(labelMat[i]!=labelMat[j]):
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C,C+alphas[j]-alphas[i])
                else:
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[j]+alphas[i])
                #
                if L==H :
                    print 'L==H'
                    continue
                #最优修改量
                eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                if eta>=0:
                    print 'eta>=0'
                    continue
                 #调整alpha[j]在0到C之间
                alphas[j] -= labelMat[j]*(Ei-Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                #对i进行修改，但是修改了与j相同但是方向相反
                if(abs(alphas[j]-alphaJold)<0.00001):
                    print 'j移动的还不够'
                    continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold-alphas[j])

                #根据alphas i和j设置常数项b
                b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*\
                    dataMatrix[i,:]*dataMatrix[i,:].T-\
                    labelMat[j]*(alphas[j]-alphaJold)*\
                    dataMatrix[i,:]*dataMatrix[j,:].T
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*\
                    dataMatrix[i,:]*dataMatrix[j,:].T-\
                    labelMat[j]*(alphas[j]-alphaJold)*\
                    dataMatrix[j,:]*dataMatrix[j,:].T
                if(0<alphas[i]) and (C>alphas[i]):
                    b=b1
                elif (0<alphas[j]) and (C>alphas[j]):
                    b=b2
                else:
                    b=(b1+b2)/2.0

                #循环次数
                alphaPairsChanged +=1
                print 'iter：%d i:%d, 改变的对数：%d' %(iter,i,alphaPairsChanged)
        if(alphaPairsChanged==0) :
            iter +=1
        else:
            iter=0
        print '外循环次数：%d' %iter
    return b,alphas

# 分类任务
def calcWs(alphas, dataArr, classLabels):
    X = mat(dataArr)
    labelMat = mat(classLabels).transpose()
    m,n=shape(X)
    w=zeros((n,1))
    for i in range(m):
        w += multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w

#main函数
if __name__=='__main__':
    data,label=loadDataSet('testSet.txt')
    b,alphas=smoSimple(data,label,0.6,0.001,40)
    print 'b: %f'%b
    count = 0
    print '支持向量：'
    for i in range(100):
        if alphas[i]>0.0:
            print data[i], label[i]
            count += 1
    print  '支持向量个数：%d' %count

    #分类任务
    ws=calcWs(alphas,data,label)
