#coding=utf-8
import numpy as np
from numpy.linalg import inv


x = np.array([[2,2,1],[-3,12,3],[8,-2,1],[2,12,4]])
# ainv = inv(x) #矩阵的逆
# a,b = np.linalg.eig(x)  #第一个是特征值,第二个是特征向量
# c = np.linalg.det(x) #行列式的值
d = np.linalg.matrix_rank(x) #矩阵的秩

# print ainv
# print a
# print b
# print c
print d