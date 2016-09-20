#coding=utf-8
'''
Created on Jun 1, 2011

@author: Peter Harrington
'''
from numpy import mat,mean,power
import  sys

def read_input(file):
    for line in file:
        yield line.rstrip()

    input=read_input(sys.stdin)
    input=[float(line) for line in input]
    numInputs=len(input)
    input=mat(input)
    sqInput=power(input,2)

