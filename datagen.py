###================================###
### gaussian data generator
### input : spec.arff
### output: data.arff
### pars N:    number of points
###      spec: path to spec.arff
###================================###
import numpy as np
import sys
import re
###================================###
### class
###================================###
class Data:
    def __init__(self,idx,coor,cls):
        self.idx=idx
        self.coor=coor
        self.cls=cls
###================================###
### function
###================================###
def getPairInt(str):
    v1,v2=0,0
    p=map(int,str.split(','))
    v1,v2=p[0],p[1]
    return v1,v2
def getPairFloat(str):
    v1,v2=0,0
    p=map(float,str.split(','))
    v1,v2=p[0],p[1]
    return v1,v2
def getNaNc(l):
    na,nc=0,0
    if re.match('@relation',l):
        ml=re.match('@relation .* \[(.*)\]',l)
        na,nc=getPairInt(ml.group(1))
    return na,nc
def getMinMax(l):
    amin,amax=0,0
    ml=re.match('@attribute.*\{(.*)\}',l)
    amin,amax=getPairFloat(ml.group(1))
    return amin,amax
def getMuSg(l):
    m,s=0,0
    ml=re.match('@class.*\[mu=(.*), \tsg=(.*)\]',l)
    m,s=float(ml.group(1)),float(ml.group(2))
    return m,s
def chkValue(v,lb,ub):
    chkmn=np.all(lb<=v)
    chkmx=np.all(v<=ub)
    return chkmn and chkmx
###================================###
### main
###================================###
if len(sys.argv)==3:
    N=int(sys.argv[1])
    sp=sys.argv[2]
else:
    print "usage: python datagen.py $N $spec"
    exit()
print ("total_points:",N," spec:",sp)

sp=open("spec.arff","r")
dt=open("data.arff","w")
###========================###
###  read header file      ###
###========================###
na,nc=0,0
na,nc=getNaNc(sp.readline())
mu=np.empty((na,nc),dtype=np.float32) #mu
sg=np.empty((na,nc),dtype=np.float32) #sigma
lb=np.empty((na,nc),dtype=np.float32) #lower-bound
ub=np.empty((na,nc),dtype=np.float32) #upper-bound
amin=np.empty(na,dtype=np.float32)
amax=np.empty(na,dtype=np.float32)
a,c=-1,0
for l in (sp.readlines()):
    if re.match('@attribute',l):
        a+=1
        c=0
        amin[a],amax[a]=getMinMax(l)
    elif re.match('@class',l):
        mu[a][c],sg[a][c]=getMuSg(l)
        c+=1
sp.close()
###========================###
### generate range         ###
###========================###
def genRange(mu,sigma):
    return mu-3*sigma,mu+3*sigma
lb,ub=genRange(mu,sg)
###========================###
### generate points        ###
###========================###
alldata=[]
chk=False
for i in range(N):
    chk=False
    c=np.random.randint(nc)
    sgt=sg[:,c].reshape(na)
    mut=mu[:,c].reshape(na)
    while not chk:
        tmp=np.random.randn(na)*sgt+mut
        chk=chkValue(tmp,lb[:,c],ub[:,c])
    d=Data(i,tmp,(c+1))
    alldata.append(d)
###========================###
### write to data.arff     ###
###========================###
#dflag="@data\n"
#dt.write(dflag)
for i in range(N):
    prt_cor,prt_data="",""
    for c in alldata[i].coor:
        prt_cor=prt_cor+str(c)+","
    prt_data=prt_cor+str(alldata[i].cls)+"\n"
    dt.write(prt_data)

dt.close()
