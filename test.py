import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import struct

class DigitaFilter:
    def __init__(self):
        self.xn = 0
        self.xn1 = [0,0,0]
        self.xn10 = [0]*10
        self.N = 10
        self.Ny = 10
        self.Xn = [0] * self.N
        self.Xny = [0] * self.N  
        self.yn = 0
        pass

    def filter(self, xn):
        y = xn - self.xn
        self.xn = xn
        return y
    def avefilter(self, xn):
        yn = xn+self.xn1[0]+self.xn1[1]+self.xn1[2]
        self.xn1[2] = self.xn1[1]
        self.xn1[1] = self.xn1[0]
        self.xn1[0] = xn
        yn=yn/4
        return yn
    def aveyfilter(self,xn):        #优化后的差分
        self.yn = yn = self.yn + xn - self.Xny[self.Ny-1]
        for i in range(self.Ny-1, 0 , -1):
            self.Xny[i] = self.Xny[i-1]
        self.Xny[0] = xn
        yn = yn/self.Ny
        return yn 

    def ave10filter(self,xn):       #10次类和的差分
        yn = xn
        for i in range(9,-1,-1):
            yn = yn + self.xn10[i]
            self.xn10[i] = self.xn10[i-1]
            self.xn10[9] = xn
        return yn/10
        
    def aveNfilter(self,xn):        #N次可调参类和差分
        yn = 0
        for i in range(0, self.N - 1):
            self.Xn[i] = self.Xn[i+1]
            yn = yn +self.Xn[i]
        self.Xn[self.N - 1] = xn
        yn = yn + xn

        return yn / self.N 


# def Average(inputs,per):
#     if np.shape(inputs)[0] % per != 0:
#         lengh = np.shape(inputs)[0] / per
#         for x in range(int(np.shape(inputs)[0],int(lengh + 1)*per)):
#             inputs = np.append (inputs,inputs[np.shape(inputs)[0]-1])
#         inputs = inputs.reshape((-1,per))
#         mean = []
#         for tmp in inputs:
#             mean.append(tmp.mean())
#         return mean

if __name__ == '__main__':
    fp = open("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/103.dat", "rb")
    fp1 = open("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/103.dat", "rb")
    fp_out = open("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/test103-out.dat", "wb")
    fp_out2 = open("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/test103-out2.dat", "wb")
    fp_out3 = open("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/test103-out3.dat", "wb")
    diff=DigitaFilter()
    for i in range(0,2500):
        x = struct.unpack('h', fp.read(2))
        y = diff.filter(x[0])
        y2 = diff.aveNfilter(x[0])
        y3 = diff.aveyfilter(x[0])
        fp_out.write(struct.pack('h', int(y)))
        fp_out2.write(struct.pack('h',int(y2)))     #N=10累和差分
        fp_out3.write(struct.pack('h',int(y3)))     #优化后的累和差分
    sentiment = []
    # fp2 = []
    # for line in fp1:
    #     fp2.append(int(line))
    # fp2.close()
    # print(fp2)


        
    fp.close()
    fp_out.close()
    fp_out2.close()
    fp_out3.close()

    ecg = np.fromfile("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/103.dat",dtype=np.short)
    ecg0 = np.fromfile("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/test103-out.dat",dtype=np.short)
    ecg1 = np.fromfile("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/test103-out2.dat",dtype=np.short)
    ecg2 = np.fromfile("H:/ZZ/其他课/智能医学仪器设计/SmartHealth/data/mitdb/test103-out3.dat",dtype=np.short)
    plt.subplot(4,1,1)
    plt.plot(ecg[0:500])
    plt.subplot(4,1,2)
    plt.plot(ecg0[0:500])
    plt.subplot(4,1,3)
    plt.plot(ecg1[0:500])
    plt.subplot(4,1,4)
    plt.plot(ecg2[0:500])
    plt.show()