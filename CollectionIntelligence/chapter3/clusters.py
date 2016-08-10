# coding=utf-8
from math import sqrt
from  PIL import Image, ImageDraw
import random

def readfile(filename):
    lines = [line for line in file(filename)]

    #第一行是标题
    colnames = lines[0].strip().split('\t')[1:]
    rownmes = []
    data = []
    for line in lines[1:]:
        p=line.strip().split('\t')
        #每行的第一列是行名
        rownmes.append(p[0])
        #剩余的是数据
        data.append([float(x) for x in p[1:]])
    return rownmes,colnames,data


def pearson(v1, v2):
    #简单求和
    sum1=sum(v1)
    sum2=sum(v2)

    #求平方和
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])

    #求乘积之和
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

    #计算r
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq - pow(sum1,2)/len(v1)) * (sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 0

    return 1.0-num/den

#用于分级聚类的类
class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left;
        self.right = right;
        self.vec = vec;
        self.id = id;
        self.distance = distance

# 聚类过程
def hcluster(rows, diatance = pearson):
    distances={}
    currentclustid=-1

    #最开始的聚类就是数据中的行
    cluster=[bicluster(rows[i],id=i) for i in range(len(rows))]   # 这个cluster相当于用数组表示的一棵树，第0个元素相当于树的根

    while len(cluster)>1:#不断合并直到最后树里面只有一个节点
        lowestpair=(0,1) # 最近的两个节点编号
        closet = diatance(cluster[0].vec, cluster[1].vec) #最近的两个点的距离

        #遍历每一个点，寻找最小距离
        for i in range(len(cluster)):
            for j in range(i+1, len(cluster)):
                #用distance缓存两个点的距离
                if (cluster[i].id, cluster[j].id) not in distances:
                    distances[(cluster[i].id, cluster[j].id)] = diatance(cluster[i].vec, cluster[j].vec)

                d = distances[(cluster[i].id,cluster[j].id)]

                #记录最近的点
                if d<closet:
                    closet = d
                    lowestpair=(i,j)
        # 计算两个聚类的平均值，新的聚类里面的词频是合并的两个聚类词频的平均值？？？？
        mergevec=[(cluster[lowestpair[0]].vec[i] + cluster[lowestpair[1]].vec[i])/2.0
                  for i in  range(len(cluster[0].vec))]
        #建立新的聚类
        newcluster = bicluster(mergevec, left= cluster[lowestpair[0]],
                               right=cluster[lowestpair[1]], distance=closet,
                               id = currentclustid)
        #不在原始集合中的聚类，其id为负数？？
        currentclustid = -1
        del cluster[lowestpair[1]] #把合并后的原来两个节点删除
        del cluster[lowestpair[0]]
        cluster.append(newcluster)

    return cluster[0]

# 打印树的结构
def printclust(clust, labels=None, n=0):
    #利用缩进来建立层次布局
    for i in range(n): print ' ',
    if clust.id<0:
        #负数表明是一个分支
        print '-'
    else:
        #正数表明是叶节点,只有遍历到达叶节点才打印节点编号，否则往栈里面加入空格和 ‘-’
        if labels==None: print clust.id
        else: print labels[clust.id]

    # 打印左子树和右子树（层次打印）
    if clust.left!=None: printclust(clust.left, labels=labels, n=n+1)
    if clust.right!=None: printclust(clust.right, labels=labels, n=n+1)

#假设树的布局是从左到右，则画面的长是树的深度，宽是树的高度
def getheight(clust):
    #这是一个叶节点吗，是则高度为1
    if clust.left==None and clust.right==None: return 1
    #否则高度为每个分支高度之和
    return getheight(clust.left)+getheight(clust.right)

def getdepth(clust):
    #叶节点距离是0
    if clust.left==None and clust.right ==None: return 0
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance

def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    #高度和宽度
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)

    #由于宽度固定的，因此需要对距离值做一些调整
    scaling=float(w-150)/depth

    #新建一个白色背景
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    #画第一个节点
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')

def drawnode(draw,clust,x,y,scaling,labels):
  if clust.id<0:
    h1=getheight(clust.left)*20
    h2=getheight(clust.right)*20
    top=y-(h1+h2)/2
    bottom=y+(h1+h2)/2
    # Line length
    ll=clust.distance*scaling
    # Vertical line from this cluster to children
    draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

    # Horizontal line to left item
    draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

    # Horizontal line to right item
    draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

    # Call the function to draw the left and right nodes
    drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
    drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
  else:
    # If this is an endpoint, draw the item label
    draw.text((x+5,y-7),labels[clust.id],(0,0,0))


#将矩阵进行转置
def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


#####kmeans聚类
def kcluster(rows,distance=pearson,k=4):
    #确定每个点的最小值和最大值
    ranges=[(min(row[i] for rom in rows), max(row[i] for row in rows))
            for i in range(len(rows[0]))]

    #随机创建k个中心点
    clusters=[[random.random() *(ranges[i][1]-ranges[i][0])+ ranges[i][0]
               for i in range(len(rows[0]))] for j in range(k)]


if __name__=='__main__':

    blognames, words, data = readfile('blogdata.txt')
    # cluster = hcluster(data)

    # printclust(cluster,labels=blognames)
    # drawdendrogram(cluster,blognames)

    #对单词聚类
    rdata=rotatematrix(data)
    wordcluster=hcluster(rdata)
    drawdendrogram(wordcluster,labels=words,jpeg='wordclust.jpg')


