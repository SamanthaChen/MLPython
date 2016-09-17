#coding=utf-8
from numpy import *

#一个简单的数据集
def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

#根据文件名获取数据
def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) #get number of fields
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

#单层决策树生成函数
# 通过阈值比较进行分类，在阈值一遍的分到-1，另一边的分到+1
#@param 数据矩阵，维度(第dimen个特征)，阈值，大于小于还是等于
def stumpClassfy(dataMatrix,dimen,threshVal,threshIneq):
    #思路是首先将全部元素置为1，再将不满足不等式的数置为-1
    retArray=ones((shape(dataMatrix)[0],1)) # n*1 n是特征数
    if threshIneq=='It':
        retArray[dataMatrix[:,dimen] <= threshVal]= -1.0  #这里面其实包含一个循环操作
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray

#单层决策树生成函数
# @param D是权重向量
def buildStump(dataArr, classLabels,D):
    dataMatrix = mat(dataArr)
    labelMat=mat(classLabels).T
    m,n=shape(dataMatrix)
    numSteps=10.0 #在特征的所有可能值上进行遍历,可能值取10个
    bestStump={} #储存给定权重D时候最佳的单层决策树的信息
    bestClassEst=mat(zeros((m,1)))
    minError=inf #最小误差

    #最外层循环遍历所有的特征
    for i in range(n):
        rangeMin=dataMatrix[:,i].min()
        rangeMax=dataMatrix[:,i].max()
        stepSize=(rangeMax-rangeMin)/numSteps #对于数值型数据，计算步长
        for j in range(-1,int(numSteps)+1):
            for inequal in ['It','gt']:
                threshVal=(rangeMin+float(j)*stepSize)
                predictedVals=stumpClassfy(dataMatrix, i, threshVal, inequal) #树桩分类器进行预测标签
                errArr=mat(ones((m,1)))
                errArr[predictedVals==labelMat]=0
                weighedError=D.T*errArr

                #打印一下当前分类结果
                #print 'Split: dim %d, thresh %.2f, thresh inequal: %s, the weidghted error is %.3f' %(i,threshVal,inequal,weighedError)

                #更新当前最小错误率
                if weighedError<minError:
                    minError=weighedError
                    bestClassEst=predictedVals.copy() #最佳的类预测
                    bestStump['dim']=i #最佳的划分特征
                    bestStump['thresh']=threshVal #最佳的划分阈值
                    bestStump['ineq']=inequal #最佳的不等式

    return bestStump,minError,bestClassEst

# 基于单层决策树的AdaBoost训练过程
def adaBoostTrainDS(dataArr, classLabels, numIt=40):
    weakClassArr=[]
    m=shape(dataArr)[0]
    D = mat(ones((m,1))/m) #初始的数据点权重
    aggClassEst=mat(zeros((m,1))) #记录每个数据点的类别估计累积值
    # 迭代
    for i in range(numIt):
        #使用权值D来训练得到基本分类器
        bestStump,error,classEst=buildStump(dataArr,classLabels,D) #
        print 'D:',D.T
        #计算基本分类器的系数alpha
        alpha=float(0.5*log((1.0-error)/max(error,1e-16))) #分类器的系数,1e-16确保不会发生除0溢出
        bestStump['alpha']=alpha
        weakClassArr.append(bestStump) #添加当前最优的弱分类器的信息
        print 'classEst: ',classEst.T
        #为下一次迭代计算D
        expon=multiply(-1*alpha*mat(classLabels).T,classEst)
        D=multiply(D,exp(expon))
        D=D/D.sum() #规范化
        #错误率累积计算，训练错误率为0的时候可以提前退出循环
        aggClassEst += alpha*classEst
        print 'aggClassEst: ',aggClassEst.T
        aggErrors=multiply(sign(aggClassEst)!=mat(classLabels).T, ones((m,1))) #错误率是误分类的变迁和
        errorRate=aggErrors.sum()/m
        print 'total error:',errorRate,'\n'
        if errorRate==0.0:break
    return weakClassArr,aggClassEst

# adaBoost分类函数
#@param 待分类样例，多个弱分类器组成的数组
def adaClassify(datToClass,classfierArr):
    datdaMatrix=mat(datToClass)
    m=shape(datdaMatrix)[0] #待分类样例个数
    aggClassEst=mat(zeros((m,1))) #运行时的类别估计值
    #遍历所有的弱分类器
    for i in range(len(classfierArr)):
        #根据弱分类器预测类别
        classEst=stumpClassfy(datdaMatrix,classfierArr[i]['dim'],classfierArr[i]['thresh'],classfierArr[i]['ineq'])
        #对弱分类器训练出来的类别按照权重相加
        aggClassEst += classfierArr[i]['alpha']*classEst
        #print aggClassEst  #打印当前的分类结果
    return sign(aggClassEst) #输出最后一个分类结果

#ROC曲线的绘制以及AUC计算函数
def plotROC(predStrengths,classLabels):
    import matplotlib.pyplot as plt
    cur=(1.0, 1.0) #光标位置
    ySum=0.0 #AUC的值
    #计算正例的个数
    numPosClas=sum(array(classLabels)==1.0)
    #分别计算x轴和y周步长]
    yStep=1/float(numPosClas)
    xStep=1/float(len(classLabels)-numPosClas)
    #获取排好序的索引,值从小到大排，但是输出的是索引
    sortedIndices=predStrengths.argsort()
    fig=plt.figure()
    fig.clf()
    ax=plt.subplot(111)
    #下面是将光标按照样例孙次进行移动，并且累计计算AUC
    for index in sortedIndices.tolist()[0]:
        if classLabels[index]==1.0:
            delX=0
            delY=yStep
        else:
            delX=xStep
            delY=0
            ySum += cur[1]
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY], c='b')
        cur=(cur[0]-delX,cur[1]-delY)
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC')
    ax.axis([0,1,0,1])
    plt.show()
    print 'AUC面积：',ySum*xStep





#main函数
if __name__=='__main__':

    #D=mat(ones((5,1))/5)
    # dataMat, classLabels = loadSimpData()
    # #bestStump,minError,bestClassEst = buildStump(dataMat,classLabels,D)
    # #print bestStump,minError,bestClassEst
    # #训练分类器
    # # classifierArray=adaBoostTrainDS(dataMat,classLabels,20)
    # #print classifierArray
    # #利用分类器进行分类
    # res = adaClassify([0,0],classifierArray)
    # print res

    #训练
    dataMat, classLabels = loadDataSet('horseColicTraining2.txt')
    classfierArray,aggClassEst=adaBoostTrainDS(dataMat,classLabels,50)
    print 'classfierArray,aggClassEst:',classfierArray,aggClassEst
    #测试
    testData,testLabel=loadDataSet('horseColicTest2.txt')
    predict10=adaClassify(testData,classfierArray)
    error=mat(ones((67,1)))
    print error[predict10!=mat(testLabel).T].sum()
    #画图
    plotROC(aggClassEst.T,classLabels)

