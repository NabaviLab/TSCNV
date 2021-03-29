import math
import statistics

from DetectFirstCP import DetectFirstCP
from astropy.table import Table
import numpy as np
import Testing

def IterativeTS(R, epsilon):
    it = 0
    pos = 0
    F = []
    n = mm = R
    while len(mm) > 0:
        epsilon = math.sqrt(statistics.variance(mm) * 2 * math.log(len(mm)))
        F,beg = DetectFirstCP(mm, epsilon)
        mm = n[beg+pos[-1]:np.size(R, 1)]
        pos = pos + [beg + pos[-1]]
        it += 1
        s = F[0:beg]
        F = F + s
    F = F + np.full(1, np.size(n,1) - np.size(F,1), np.mean(R[np.size(F,1)]))
    pos_temp = np.abs(np.diff(F))
    pos = np.where(pos_temp != 0 and pos_temp > 0.1)
    ipt = pos
    in_temp = np.diff(ipt)
    int = np.where(in_temp != 0 and in_temp < 100)
    for i in int:
        ipt[i] = []
    rows = 0
    if len(ipt) % 2 == 0:
        rows = len(ipt)/2
    else:
        rows = len(ipt+1)/2
    ipts = np.resize(ipt, (rows, 2))
    mm = n
    denoised = []
    logcopR = []
    denoised[0:ipts[0,0]-1] = np.mean(mm[0:ipts[0,0]-1])
    for f in range(len(ipt)-2):
        denoised[ipt[f]-1:ipt[f+1]-1] = np.mean(mm[ipt[f]-1:ipt[f+1]-1])
        logcopR[f] = np.mean(mm[ipt[f]-1:ipt[f+1]-1])
    denoised[ipt[-1]-1:len(mm)] = np.mean(mm[ipt[-1]-1:len(mm)])
    logcopR = [np.mean(mm[0:ipts[0,0]-1])] + logcopR + [np.mean(mm[ipt(-1):len(mm)])]
    start = [1] + ipt
    stop = [ipt-1] + [len(mm)]
    logipt = []
    for g in range(1, np.size(ipts,1)):
        logipt[g-1] = np.mean(mm[ipts[g-1,0]:ipts[g-1,1]])
    
    CNVList = Table([start, stop, logcopR], names=('Start', 'Stop', 'Copynumber'))
    return F, CNVList


#Testing

length = 1000
sections = 5
sec_length = int(length/sections)
data1 = Testing.makeData(sections, sec_length)
noise1 = Testing.makeNoise(length, 0.05)
new_data = Testing.addNoise(data1, noise1)
r, ep = IterativeTS(new_data, 0.05)