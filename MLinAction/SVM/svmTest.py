#coding=utf-8
import random
from numpy import *
def loadDataSet(fileName):
    '''
    记载数据
    :param fileName:
    :return:
    '''
    dataMat=[]
    labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m):
    '''
    从0-m的范围随机生成一个不等于i的数
    :param i:
    :param m:
    :return:
    '''
    j=i
    while j==i:
        j=int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    '''
    将aj限定在L和H之间
    :param aj:
    :param H:
    :param L:
    :return:
    '''
    if aj>H:
        aj=H
    if aj<L:
        aj=L
    return aj

def somSimple(dataMatIn,classLabels, C, toler, maxIter):
    '''
    简化版的SMO算法，两个alpha是随机选的
    :param dataMatIn:
    :param classLabels:
    :param C:
    :param toler:
    :param maxIter:
    :return:
    '''
    dataMatrix=mat(dataMatIn)
    labelMat=mat(classLabels).transpose()
    b=0
    m,n=shape(dataMatrix)
    alphas=mat(zeros((m,1)))#alpha初值是0
    iter=0
    while (iter<maxIter):
        alphaPairChanged=0 #一对alpha被修改的标识
        for i in range(m):
             fXi=float(multiply(alphas,labelMat).T * (dataMatrix*dataMatrix[i,:].T))+b
             Ei=fXi-float(labelMat[i])
             #如果误差很大，需要对alpha进行优化,不管是正间隔还是负间隔都需要进行计算
             if((labelMat[i]*Ei<-toler) and (alphas[i]<C)) or ((labelMat[i]*Ei>toler) and (alphas[i]>0)):
                 #随机选择第二个alpha
                 j=selectJrand(i,m)
                 fXj=float(multiply(alphas,labelMat).T * (dataMatrix*dataMatrix[j,:].T))+b
                 Ej=fXj-float(labelMat[j])
                 #保存老的alpha值
                 alphaIold=alphas[i].copy()
                 alphaJold=alphas[j].copy()
                 #保证alpha在0到c之间
                 if(labelMat[i]!=labelMat[j]):
                     L=max(0,alphas[j]-alphas[i])
                     H=min(C,C+alphas[j]-alphas[i])
                 else:
                     L=max(0,alphas[j]+alphas[i]-C)
                     H=min(C,alphas[j]+alphas[i])

                 if L==H: print 'L==H';continue;
                 eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                 if eta>=0 : print 'eta>=0';continue;
                 alphas[j] -= labelMat[j]*(Ei-Ej)/eta
                 #剪辑
                 alphas[j]=clipAlpha(alphas[j],H,L)
                 if(abs(alphas[j]-alphaJold)<0.00001) :
                     print 'j not moving enough'
                     continue
                 alphas[i] += labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                 #每次完成两个alpha的优化后，需要设置常数项
                 b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                 b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                 if(0<alphas[i]) and (C>alphas[i]):
                    b=b1
                 elif (0<alphas[j]) and (C>alphas[j]):
                    b=b2
                 else:
                    b=(b1+b2)/2.0
                #循环次数
                 alphaPairChanged +=1
                 print 'iter：%d i:%d, 改变的对数：%d' %(iter,i,alphaPairsChanged)
        if(alphaPairChanged==0) :
             iter +=1
        else:
            iter=0
        print '外循环次数：%d' %iter
    return b,alphas



