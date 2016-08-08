#coding=utf-8
__author__ = 'SamanthaChen'
'''
：http://blog.csdn.net/daringpig/article/details/8072794
http://www.52nlp.cn/hmm-learn-best-practices-five-forward-algorithm-5

三枚硬币，随机选择一枚，进行抛掷，记录抛掷结果。
可以描述为一个三个状态的隐马尔科夫模型l。
l = (S, V, A, B, p)，其中
S = {1, 2, 3}
V = {H,T}
A 如下表所示 B 如下表所示
    1    2         3
A = 0.9, 0.05, 0.05
    0.45, 0.1, 0.45
    0.45, 0.45,0.1
B =
head   0.5, 0.75, 0.25
tail   0.5,0.25,0.75

O = (H H H H T H T T T T)

'''
'HMM的前向算法实现，计算给定观察序列的概率'
def forward(hiddentS,observedS, intitialS, transM, confuseM,observeSequence):

    M = len(hiddenS)  # 隐藏状态变量个数
    N = len(observeSequence) # 输出的状态数目
    alpha = [[0 for col in range(N)] for row in range(M)] #前向概率矩阵 M行N列

    # 先将观察序列处理成对应的下标
    obS = [] #里面存的是状态对应的索引
    for s in observeSequence:
        obS.append(observedS.index(s))


    # 初始化alpha
    for i in range(M):
        alpha[i][0] = initialS[i] * confuseM[i][obS[0]]

    # 计算后面的概率
    for j in range(1,N): #对于每个观测状态 列
        for i in range(0,M): # 对于每个隐藏状态 行
            temp = 0
            for k in range(0,M):
                temp += alpha[k][j-1] * transM[k][i] # 上一次k转移到i的概率
            alpha[i][j] = temp*confuseM[i][obS[j]]

    print alpha
    # 计算最终的概率
    res = 0
    for i in range(M):
        res += alpha[i][N-1]

    print res

'后向算法'
def backward(hiddentS,observedS, intitialS, transM, confuseM,observeSequence):
    # 先将观察序列处理成对应的下标
    obS = [] #里面存的是状态对应的索引
    for s in observeSequence:
        obS.append(observedS.index(s))

    M = len(hiddenS)  # 隐藏状态变量个数
    N = len(observeSequence) # 输出的状态数目
    beta = [[0 for col in range(N+1)] for row in range(M)] #后向概率矩阵 M行N+1列

    #初始化最后一列
    for i in range(M):
        beta[i][N] = 1

    # 计算后向概率
    for j in range(N-1,0,-1): # 从后往前计算,第j个输出状态
        for i in range(M):
            for k in range(M):
                beta[i][j] += transM[i][k]*confuseM[k][obS[j]]*beta[k][j+1]



    # 计算第一个的概率
    res = 0
    for i in range(M):
        beta[i][0] = intitialS[i]*confuseM[i][obS[0]]*beta[i][1]
        res += beta[i][0]

    print beta
    print res


# 解码问题的维特比算法
def viterbi(hiddenS,observedS, initialS, transM, confuseM,observeSequence):
    # 先将观察序列处理成对应的下标
    obS = [] #里面存的是状态对应的索引
    for s in observeSequence:
        obS.append(observedS.index(s))

    M = len(hiddenS)  # 隐藏状态变量个数
    N = len(observeSequence) # 输出的状态数目

    theta  = [[0 for col in range(N)] for row in range(M)] #似然概率矩阵 M行N列
    path  = [[0 for col in range(N)] for row in range(M)] #路径矩阵 M行N列

    # 计算初始概率
    for i in range(M):
        theta[i][0] = initialS[i]*confuseM[i][obS[0]]

    # 计算极大似然概率
    for j in range(1,N):
        for i in range(0,M):
            maxp = 0 # 最大概率
            for k in range(0,M):
                temp = theta[k][j-1] * transM[k][i]  *  confuseM[i][obS[j]]
                if(temp>maxp) :
                    path[i][j] = k
                    maxp = temp
            theta[i][j] = maxp

    # 回溯计算最佳路径

    #最后一列找最大
    index = 0
    maxp = 0
    for i in range(M):
        if(theta[i][N-1]>maxp):
            maxp = theta[i][N-1]
            index = i #找最大的一个索引

    s =  hiddenS[index]
    for j in range(N-1,0,-1):
        index = path[index][j]
        s = hiddenS[index]+'->' +s

    print theta
    print maxp
    print path
    print s



if __name__ == '__main__':
    hiddenS = ['1','2','3'] #隐藏状态
    observedS = ['H','T'] #观测状态
    transM = [[0.9, 0.05, 0.05],[0.45, 0.1, 0.45],[0.45, 0.45,0.1]] #观测序列的转移状态
    confuseM = [ [0.5,0.5],[0.75,0.25],[0.25,0.75]] #横轴对应的是隐藏状态，纵轴对应的是观察序列
    initialS = [1.0/3.0,1.0/3.0,1.0/3.0]
    observeSequence = ['H','H',  'T']
    # forward(hiddenS,observedS, initialS, transM, confuseM,observeSequence)
    # backward(hiddenS,observedS, initialS, transM, confuseM,observeSequence)
    viterbi(hiddenS,observedS, initialS, transM, confuseM,observeSequence)
