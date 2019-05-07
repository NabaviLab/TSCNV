import numpy as np
import math
import statistics as st
def firstCP(n,epsilon):
    N=length(n)
    if N<=1:
        s=n
        return
    s=np.zeros(np.shape(n))
    lowindex=np.zeros(1,N)
    upindex=np.zeros(1,N)
    allcp=[]
    lowindexcounts = 1
    upindexcounts = 1
    cpn = 1
    indcpn = 1
    lowindex[0] = 1
    lowerinit = n[0]-epsilon
    upperinit = n[0]+epsilon
    lowerlast = lowerinit
    upperlast = upperinit
    for i in range(2,N-1):
        if n[i]>=lowerlast:
            if n[i]<=upperlast:
                upperlast=upperlast+(n[i]-upperlast)/(i-upindex[upindexcounts]+1)
                s[indcpn]=upperinit
                allcp.append(indcpn)
                if indcpn!=1:
                    break
                while (upindexcounts>cpn) and (upperlast<=s[upindex[upindexcounts-1]]):
                    upindexcounts=upindexcounts-1
                    upperlast=s[upindex[upindexcounts]]+(upperlast-s[upindex[upindexcounts]])*((i-upindex[upindexcounts+1]+1)/(i-upindex[upindexcounts]+1))
                if upindexcounts==cpn:
                    while (upperlast<=lowerinit) and (cpn<lowindexcounts):
                        cpn=cpn+1
                        s[indcpn:lowindex[cpn]-1]=lowerinit
                        upperlast=upperlast+(upperlast-lowerinit)*((lowindex[cpn]-indcpn)/(i-lowindex[cpn]+1))
                        indcpn=lowindex[cpn]
                        lowerinit=s[indcpn]
                    
                    upperinit=upperlast
                    upindexcounts=cpn
                    upindex[cpn]=indcpn
                else:
                   s[upindex[upindexcounts]]=upperlast
            else:
                upindexcounts=upindexcounts+1
                upindex(upindexcounts)=i
                s[i]=n[i]
                upperlast=s[i]
            lowerlast=lowerlast+(n[i]-lowerlast)/(i-lowindex[lowindexcounts]+1)
            s[indcpn]=lowerinit
            while (lowindexcounts>cpn) and (lowerlast>=s[lowindex[lowindexcounts-1]]):
                lowindexcounts=lowindexcounts-1
                lowerlast=s[lowindex[lowindexcounts]]+(lowerlast-s[lowindex[lowindexcounts]])*((i-lowindex[lowindexcounts+1]+1)/(i-lowindex[lowindexcounts]+1))
            if lowindexcounts==cpn:
                while (lowerlast>=upperinit) and (cpn<upindexcounts):
                    cpn=cpn+1
                    s[indcpn:upindex[cpn]-1]=upperinit
                    lowerlast=lowerlast+(lowerlast-upperinit)*((upindex[cpn]-indcpn)/(i-upindex[cpn]+1))
                    indcpn=upindex[cpn]
                    upperinit=s[indcpn]
                lowerinit=lowerlast
                lowindexcounts=cpn
                lowindex[cpn]=indcpn
                if indcpn==i:
                  lowerinit=upperinit-2*epsilon
            else:
                s[lowindex[lowindexcounts]]=lowerlast
        else:
            lowindexcounts = lowindexcounts+1
            lowindex[lowindexcounts] = i
            s[i]=n[i]
            lowerlast=s[i]
            upperlast=upperlast+(n[i]-upperlast)/(i-upindex[upindexcounts]+1)
            s[indcpn]=upperinit
            while (upindexcounts>cpn) and (upperlast<=s[upindex[upindexcounts-1]]):
                upindexcounts=upindexcounts-1
                upperlast=s[upindex[upindexcounts]]+(upperlast-s[upindex[upindexcounts]])*((i-upindex[upindexcounts+1]+1)/(i-upindex[upindexcounts]+1))
            if upindexcounts==cpn:
                while (upperlast<=lowerinit) and (cpn<lowindexcounts):
                    cpn=cpn+1
                    s[indcpn:lowindex[cpn]-1]=lowerinit
                    upperlast=upperlast+(upperlast-lowerinit)*((lowindex[cpn]-indcpn)/(i-lowindex[cpn]+1))
                    indcpn=lowindex[cpn]
                    lowerinit=s[indcpn]
                upperinit=upperlast
                upindexcounts=cpn
                upindex[cpn]=indcpn
                if indcpn==i:
                    upperinit=lowerinit+2*epsilon
            
            else:
                s[upindex[upindexcounts]]=upperlast
    i=N
    if n[i]+epsilon<=lowerlast:
        while cpn<lowindexcounts:
            cpn=cpn+1
            s[indcpn:lowindex[cpn]-1] = lowerinit
            indcpn=lowindex[cpn]
            lowerinit=s[indcpn]
    elif n[i]-epsilon>=upperlast:
        while cpn<upindexcounts:
            cpn=cpn+1
            s[indcpn:upindex[cpn]-1] = upperinit
            indcpn=upindex[cpn]
            upperinit=s[indcpn]
    else:
        lowerlast=lowerlast+(n[i]+epsilon-lowerlast)/(i-lowindex[lowindexcounts]+1)
        s[indcpn]=lowerinit
        while (lowindexcounts>cpn) and (lowerlast>=s[lowindex[lowindexcounts-1]]):
            lowindexcounts=lowindexcounts-1
            lowerlast=s[lowindex[lowindexcounts]]+(lowerlast-s[lowindex[lowindexcounts]])*((i-lowindex[lowindexcounts+1]+1)/(i-lowindex[lowindexcounts]+1))
        if lowindexcounts==cpn:
            if upperinit>=lowerlast:
                s[indcpn:i]=lowerlast
            else:
                upperlast=upperlast+(n[i]-epsilon-upperlast)/(i-upindex[upindexcounts]+1)
                s[indcpn]=upperinit
                while (upindexcounts>cpn) and (upperlast<=s[upindex[upindexcounts-1]]):
                    upindexcounts=upindexcounts-1
                    upperlast=s[upindex[upindexcounts]]+(upperlast-s[upindex[upindexcounts]])*((i-upindex[upindexcounts+1]+1)/(i-upindex[upindexcounts]+1))
                
                s[upindex[upindexcounts]:i)=upperlast
                while cpn<upindexcounts:
                    cpn=cpn+1
                    s[indcpn:upindex[cpn]-1] = upperinit
                    indcpn=upindex[cpn]
                    upperinit=s[indcpn]
        else:
            s[lowindex[lowindexcounts]:i]=lowerlast
            while cpn<lowindexcounts:
                cpn=cpn+1
                s[indcpn:lowindex[cpn]-1] = lowerinit
                indcpn=lowindex[cpn]
                lowerinit=s[indcpn]
    firscp=allcp[allcp!=1]
    return s,firstcp

                
                
            
            
                
                
                
        
            
            
    
    
        
            
            
                  
                    
                    
                    
                
            
            
            
                
                
                    
                    
                
                
                
                                    
                                    
            
            
            
            
                    
                    
