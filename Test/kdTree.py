#coding=utf-8
'''
kd树的数据结构构造,不能用啊尼玛
'''
import numpy
import math
class KD_node:
    def __init__(self, point=None, split=None,LL=None,RR=None):
        '''
        KD树的类
        :param point: 数据点
        :param split: 划分域
        :param LL: 左儿子
        :param RR: 右儿子
        :return:
        '''
        self.point=point
        self.split=split
        self.left=LL
        self.right=RR

def createKDTree(data_list):
        '''
        递归的创建树
        :param root: 当前树的根节点
        :param data_list: 数据点的集合（无序）
        :return:构造的kd树的树根
        '''
        LEN=len(data_list)
        #递归结束条件
        if LEN==0:
            return
        #数据点的维度
        dimension=len(data_list[0])
        #方差
        max_var=0
        #最后选择划分域
        split=0
        #计算每个维度的方差，选择最大的作为划分维度
        for i in range(dimension):
            l1=[]
            for t in data_list:
                l1.append(t[i])
            var=computeVariance(l1)
            if var>max_var:
                max_var=var
                split=i

        #根据划分域来对数据点进行排序
        data_list.sort(key=lambda  x: x[split])
        #选择下标为len/2(中位数)的作为分割点
        point=data_list[LEN/2]
        root=KD_node(point,split)
        root.left=createKDTree(root.left,data_list[0:(LEN/2)])
        root.right=createKDTree(root.right,data_list[(LEN/2+1):LEN])
        return root

def computeVariance(arrayList):
        '''
        计算方差
        :param arrayList: 存放的数据点
        :return: 返回数据点的方差
        '''
        for ele in arrayList:
            ele=float(ele)
        LEN=len(arrayList)
        array=numpy.array(arrayList)
        sum1=array.sum()
        array2=array*array
        sum2=array2.sum()
        mean=sum1/LEN
        #D(x)=E(x^2)-(E(x)^2)
        variance=sum2/LEN-mean**2
        return variance

def findNN(root,query):
    '''
    kd树的查找(最近邻查找，不是k近邻)
    :param root:树根
    :param query: 查询点
    :return:返回距离最近的点NN，并同时返回最近的距离
    '''
    #初始化为root的节点
    NN=root.point
    min_dist=computeDist(query,NN)
    nodeList=[]
    temp_root=root
    #二分查找建立路径
    while temp_root:
        nodeList.append(temp_root) #查找到节点的路径
        dd=computeDist(query,temp_root.point) #当前距离
        if min_dist>dd:
            NN=temp_root.point
            min_dist=dd
        #当前节点的划分域
        ss=temp_root.split
        if query[ss]<=temp_root.point[ss]:
            temp_root=temp_root.left
        else:
            temp_root=temp_root.right
    ##回溯查找
    while nodeList:
        #使用list模拟栈，后进先出
        back_point=nodeList.pop()
        ss=back_point.split
        print "back.point=",back_point
        #判断是否要进入父节点的子空间进行搜索
        #判断的依据就是当前点到最近点的距离d是否大于当前点到分割面（在二维空间中实际是一条直线）的距离L
        #如果d<L 没有必要进入另一个子空间，直接向上一层回溯
        #否则说明子空间中可能存在更近的点
        if abs(query[ss]-back_point.point[ss])<min_dist:
            if query[ss]<=back_point[ss]:
                temp_root=back_point.right
            else:
                temp_root=back_point.left

            if temp_root:
                nodeList.append(temp_root)
                curDist=computeDist(query,temp_root.point)
                if min_dist>curDist:
                    min_dist=curDist
                    NN=temp_root.point
    return NN,min_dist


def computeDist(pt1,pt2):
    '''
    计算两个点之间的欧几里德距离
    :param pt1:
    :param pt2:
    :return:
    '''
    sum=0.0
    for i in range(len(pt1)):
        sum = sum+(pt1[i]-pt2[i])*(pt1[i]-pt2[i])
    return math.sqrt(sum)

def KNN(list,query):
    min_dist=9999.0
    NN=list[0]
    for pt in list:
        dist=computeDist(query,pt)
        if dist<min_dist:
            NN=pt
            min_dist=dist
    return NN,min_dist

if __name__=='__main__':
    T = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
    print KNN(T,[9,4])
    root=createKDTree(T)
    print findNN(root,[9,4])
    # root=KD_node([7,2])
    # kd_tree = createKDTree(root,T)
    # query=[9,4]
    # print findNN(root,query)