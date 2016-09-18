#coding=utf-8
'''
2016.7.27 samanthachen
'''

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

#创建初始候选项集合
def createC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset,C1)

#计算支持度,C1生成L1
def scanD(D,Ck,minSuport):
    ssCnt={}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                #如果字典还没出现就添加，否则加1
                if not ssCnt.has_key(can):ssCnt[can]=1
                else: ssCnt[can] +=1
    numItems = float(len(D))
    retList=[]
    supportData={} #列表，存Lk和支持度
    for key in ssCnt:
        support=ssCnt[key]/numItems
        if support>=minSuport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData

#生成候选项集，即Lk生成Ck+1
def aprioriGen(Lk, k):
    retList=[]
    lenLk=len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            #前k-2个项相同，最后一个不同的时候，进行合并
            L1=list(Lk[i])[:k-2]
            L2=list(Lk[j])[:k-2]
            L1.sort();L2.sort();
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList

#扫描数据集，从Ck生成Lk
#完整的Apriori算法
def apriori(dataSet, minSupport=0.5):
    C1=createC1(dataset)
    D=map(set,dataset)
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1] #[[]]
    k=2
    #当不能再生成频繁项集Lk时候停止
    while(len(L[k-2])>0):
        Ck=aprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minSupport) #按照支持度剪掉不频繁的
        supportData.update(supK) #插入新的{Lk，支持度}
        L.append(Lk)
        k +=1
    return L,supportData

#关联规则生成函数
def generateRules(L,supportData,minConf=0.7):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]: #freqSet是长度为i的频繁项集列表
            H1=[frozenset([item]) for item in freqSet] #先创建只含有单个元素的列表H1
            #获取只有两个或者更多的元素集合来生成规则
            if i>1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf) #如果项集中只含有两个元素，就直接计算
    return bigRuleList

#生成候选规则集合
#@param freqSet是频繁项集集合，H是可以出现在规则右边的列表（其实也是频繁项集）
def rulesFromConseq(freqSet, H, supportData, bigRuleList, minConf):
    m=len(H[0])
    if(len(freqSet)>(m+1)):#前件至少要大于1的长度
        Hmp1=aprioriGen(H,m+1) #生成Lk
        Hmp1=calcConf(freqSet,Hmp1,supportData,bigRuleList,minConf)
        if (len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,bigRuleList,minConf)



#对规则进行评估,保存满足最小可信度的规则后件
def calcConf(freqSet,H,supportData,bigRuleList,minConf):
    prunedH=[]
    for conseq in H: #conseq是后件，freqSet-conseq是前件
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print freqSet-conseq,'-->',conseq,' conf: ',conf
            bigRuleList.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH
#main
if __name__=='__main__':
    dataset=loadDataSet()
    L,supportData=apriori(dataset,0.5)
    print L[0],'\n',L[1],'\n',L[2]
    print supportData
    rules=generateRules(L,supportData,0.7)
