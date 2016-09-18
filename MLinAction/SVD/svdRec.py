#coding=utf-8
'''
Created on Jun 1, 2011

@author: Peter Harrington
'''
from numpy import *

def loadExData():
    return[
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 0, 0, 0],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1]]

def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

#main
if __name__=='__main__':
    data = loadExData();
    U,Sigma,VT = linalg.svd(data)
    print Sigma
    #重构矩阵
    sigma2 = mat([ [Sigma[0],0,0],[0,Sigma[1],0],[0,0,Sigma[2]]])
    reconData = U[:,:3]*sigma2*VT[:3,:]
    print data
    print reconData