def DetectFirstCP(R, epsilon):
    N = len(R)
    if N <= 1:
        F = R
        return F, []
    F = [0] * N

    changepoints = []
    F_low_first = R[0] - epsilon
    F_up_first = R[0] + epsilon 
    seglow = 1
    segup = 1
    segnum = 1
    indsegnum = 1
    firstlowind = [1]
    firstupind = [1]
    firstlowind = [0] * N
    firstupind = [0] * N
    F_lastlow = F_low_first
    F_lastup = F_up_first
    loop_range = list(range(2, N))
    for i in loop_range:
        if R[i-1] >= F_lastlow:
            if R[i-1] <= F_lastup:
                F_lastup = F_lastup + (R[i-1] - F_lastup) / (i - firstupind[segup-1] + 1)
                F[indsegnum-1] = F_up_first
                changepoints = changepoints + [indsegnum]
                if indsegnum != 1:
                    break
                while ((segup > segnum) and (F_lastup <= F[firstupind[segup-2]-1])):
                    segup -= 1
                    F_lastup = (F[firstupind[segup-1]-1] + (F_lastup - F[firstupind[segup-1]-1]) * 
                                ((i - firstupind[segup]+1) / (i - firstupind[segup-1]+1)))
                if segup == segnum:
                    while ((F_lastup <= F_low_first) and (segnum < seglow)):
                        segnum += 1
                        F[indsegnum-1:firstlowind[segnum-1]-1] = F_low_first
                        F_lastup = (F_lastup + (F_lastup - F_low_first) *
				    		        ((firstlowind[segnum-1] - indsegnum) / (i - firstlowind[segnum-1]+1)))
                        indsegnum = firstlowind[segnum-1]
                        F_low_first = F[indsegnum-1]
                    F_up_first = F_lastup
                    segup = segnum
                    firstupind[segnum-1] = indsegnum
                else:
                    F[firstupind[segup-1]-1] = F_lastup
            else:
                segup += 1
                firstupind[segup-1] = i
                F[i-1] = R[i-1]
                F_lastup = F[i-1]
            F_lastlow = F_lastlow + (R[i-1] - F_lastlow) / (i - firstlowind[seglow-1]+1)
            F[indsegnum-1] = F_low_first
            while ((seglow > segnum) and (F_lastlow >= F[firstlowind[seglow-2]-1])):
                seglow -= 1
                F_lastlow = (F[firstlowind[seglow-1]-1] + (F_lastlow - F[firstlowind[seglow-1]-1]) *
	        		        ((i - firstlowind[seglow]+1) / (i - firstlowind[seglow-1]+1)))
            if seglow == segnum:
                while ((F_lastlow >= F_up_first) and (segnum < segup)):
                    segnum += 1
                    Flist = [F_up_first] * len(F[indsegnum-1:firstupind[segnum-1]-1])
                    F[indsegnum-1:firstupind[segnum-1]-1] = Flist
                    F_lastlow = (F_lastlow + (F_lastlow - F_up_first) *
			    		        ((firstupind[segnum-1] - indsegnum) / (i - firstupind[segnum-1]+1)))
                    indsegnum = firstupind[segnum-1]
                    F_up_first = F[indsegnum-1]
                F_low_first = F_lastlow
                seglow = segnum
                firstlowind[segnum-1] = indsegnum
                if indsegnum == i:
                    F_low_first = F_up_first-2 * epsilon
                else:
                    F[firstlowind[seglow-1]-1] = F_lastup
                seglow += 1
                firstlowind[seglow-1] = i
                F[i-1] = R[i-1]
                F_lastlow = F[i-1]
                F_lastup = F_lastup + (R[i-1] - F_lastup) / (i - firstupind[segup-1]+1)
                F[indsegnum-1] = F_up_first
                while ((segup > segnum) and (F_lastup <= F[firstupind[segup-2]])):
                    segup -= 1
                    F_lastup = (F[firstupind[segup-1]-1] + (F_lastup - F[firstupind[segup-1]-1]) *
	        		            ((i - firstupind[segup]+1) / (i - firstupind[segup-1]+1)))
                if segup == segnum:
                    while ((F_lastup <= F_low_first) and (segnum < seglow)):
                        segnum += 1
                        Flist = [F_low_first] * len(F[indsegnum-1:firstlowind[segnum-1]-1])
                        F[indsegnum-1:firstlowind[segnum-1]-1] = Flist
                        F_lastup = (F_lastup + (F_lastup - F_low_first) * 
			    		            ((firstlowind[segnum-1] - indsegnum) / (i - firstlowind[segnum-1]+1)))
                        indsegnum = firstlowind[segnum-1]
                        F_low_first = F[indsegnum-1]
                    F_up_first = F_lastup
                    segup = segnum
                    firstupind[segnum-1] = indsegnum
                    if indsegnum == i:
                        F_up_first = F_low_first+2 * epsilon
                else:
                    F[firstupind[segup-1]-1] = F_lastup
    i = N
    if (R[i-1] + epsilon <= F_lastlow):
        while segnum < seglow:
            segnum += 1
            Flist = [F_low_first] * len(F[indsegnum-1:firstlowind[segnum-1]-1])
            F[indsegnum-1:firstlowind[segnum-1]-1] = Flist
            indsegnum = firstlowind[segnum-1]
            F_low_first = F[indsegnum-1]
        Flist = [F_low_first] * len(F[indsegnum-1:i-1])
        F[indsegnum-1:i-1] = Flist
        F[i-1] = R[i-1] + epsilon
    elif (R[i-1] - epsilon >= F_lastup):
        while segnum < segup:
            segnum += 1
            Flist = [F_up_first] * len(F[indsegnum-1:firstupind[segnum-1]-1])
            F[indsegnum-1:firstupind[segnum-1]-1] = Flist
            indsegnum = firstupind[segnum-1]
            F_up_first = F[indsegnum-1]
        Flist = [F_up_first] * len(F[indsegnum-1:i-1])
        F[indsegnum-1:i-1] = Flist
        F[i-1] = R[i-1] - epsilon
    else:
        F_lastlow += (R[i-1] + epsilon - F_lastlow) / (i - firstlowind[seglow-1]+1)
        F[indsegnum-1] = F_low_first
        while ((seglow>segnum) and (F_lastlow>=F[firstlowind[seglow-2]-1])):
            seglow -= 1
            F_lastlow = (F[firstlowind[seglow-1]-1] + (F_lastlow - F[firstlowind[seglow-1]-1]) *
        		((i - firstlowind[seglow]+1) / (i - firstlowind[seglow-1]+1)))
        if seglow == segnum:
            if F_up_first >= F_lastlow:
                Flist = [F_lastlow] * len(F[indsegnum-1:i])
                F[indsegnum-1:i] = Flist
            else:
                F_lastup += (R[i-1] - epsilon - F_lastup) / (i - firstupind[segup-1]+1)
                F[indsegnum-1] = F_up_first
                while ((segup > segnum) and (F_lastup <= F[firstupind[segup-2]])):
                    segup -= 1
                    F_lastup = (F[firstupind[segup-1]-1] + (F_lastup - F[firstupind[segup-1]-1]) *
	        			        ((i - firstupind[segup]+1) / (i - firstupind[segup-1]+1)))
                Flist = [F_lastup] * len(F[firstupind[segup-1]-1:i])
                F[firstupind[segup-1]-1:i] = Flist
                while segnum < segup:
                    segnum += 1
                    Flist = [F_up_first] * len(F[indsegnum-1:firstupind[segnum-1]-1])
                    F[indsegnum-1:firstupind[segnum-1]-1] = Flist
                    indsegnum = firstupind[segnum-1]
                    F_up_first = F[indsegnum-1]
        else:
            F[firstlowind[seglow-1]-1:i] = F_lastlow
            while segnum < seglow:
                segnum += 1
                Flist = [F_low_first] * len(F[indsegnum-1:firstlowind[segnum-1]-1])
                F[indsegnum-1:firstlowind[segnum-1]-1] = Flist
                indsegnum = firstlowind[segnum-1]
                F_low_first = F[indsegnum-1]

    Firstseg = changepoints.index(1)
    return F, Firstseg
