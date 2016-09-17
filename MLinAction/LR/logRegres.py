#coding=utf-8
from numpy import *

def loadDataSet():
    dataMat=[]
    labelMat=[]
    fr=open('testSet.txt')
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])  #第一个1.0是b的系数X0
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmod(inX):
    return 1.0/(1+exp(-inX))

# 批量梯度上升法（一次更新所有样本的梯度）
def gradAscent(dataMatIn, classLabels):
    # 转换为numpy类型
    dataMatrix = mat(dataMatIn)
    print dataMatrix.shape
    labelMat = mat(classLabels).transpose()
    print labelMat.shape
    m,n=shape(dataMatrix) #m个实例，n个特征
    alpha=0.001  # 梯度移动的步长
    maxCycles = 500 #最大迭代次数
    weights = ones((n,1)) # 初始化权重为1
    print weights.shape
    for k in range(maxCycles):
        h=sigmod(dataMatrix*weights) # h =  w*x 两个矩阵相乘
        error = (labelMat-h) #真实值与预测值之间的差别
        weights = weights + alpha*dataMatrix.transpose()*error
    return weights

# 随机梯度上升fa
def stocGradAscent0(dataMatrix, classLabel):
    m,n=shape(dataMatrix) # m是样本数量，n是特征个数
    alpha=0.01
    weights=ones(n)
    for i in range(m):
        h=sigmod(sum(dataMatrix[i]*weights))
        error=classLabel[i]-h
        weights= weights+alpha*error*dataMatrix[i]
    return weights

# 改进的随机梯度上升
def stocGradAscent1(dataMatrix, classLabel,numIter=150):
    m,n=shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex=range(m) #1到m的数组
        for i in range(m):
            alpha=4/(1.0+j+i)+0.01
            randIndex=int(random.uniform(0,len(dataIndex)))  #按照均匀分布随机选一个数组元素
            print randIndex
            h=sigmod(sum(dataMatrix[randIndex]*weights))
            error=classLabel[randIndex]-h
            weights=weights+alpha*error*dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return  weights

#逻辑回归分类函数
def classifyVector(inX, weights):
    prob = sigmod(sum(inX*weights))
    if prob>0.5:return 1.0
    else:return 0.0

#预测病马的死亡率
def colicTest():
    #处理训练集和测试集
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainingSet = []
    trainingLabels = []
    for line in frTrain.readlines():
        currLine=line.strip().split('\t')
        lineArr=[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    #用逻辑回归进行训练
    trainWeights = stocGradAscent1(array(trainingSet),trainingLabels,500)
    #测试集计算错误率
    errorCount=0
    numTestVec=0.0
    for line in frTest.readlines():
        numTestVec +=1.0
        currLine=line.strip().split('\t')
        lineArr=[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr),trainWeights))!=int(currLine[21]):
            errorCount +=1
        erroRate=(float(errorCount)/numTestVec)
        print '错误率：%f' %erroRate
        return erroRate

# 多次测试求平均值
def multiTest():
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest()
    print " %d 次迭代后平均错误率是: %f" % (numTests, errorSum/float(numTests))




# 画图
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()


if __name__=='__main__':
    # dataArr,labelMat=loadDataSet()
    # w1= gradAscent(dataArr,labelMat) # 批量梯度更新
    # w2=stocGradAscent0(array(dataArr),labelMat)
    #
    # plotBestFit(w1.getA())
    # plotBestFit(w2)
    multiTest()

