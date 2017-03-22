###================================###
### data spec generator
### output: spec.arff, head.arff
### pars na:   number of attributes
###      nc:   number of classes
###      span: span mus
###      cmpr: compress sigma
###      dist: uniform/gaussian
###================================###
import numpy as np
import sys

if len(sys.argv)==6:
    na=int(sys.argv[1])
    nc=int(sys.argv[2])
    span=int(sys.argv[3])
    cmpr=int(sys.argv[4])
    dist=sys.argv[5]
else:
    print "usage:python specgen.py $na $nc $span $cmpr $dist"
    exit()
print ("num_attr:{0:4d} num_class:{1:4d}\
        span:{2:3d} cmpr:{3:2d} dist:{4}".format(na,nc,span,cmpr,dist))

mu=np.empty((na,nc),dtype=np.float32) #mu
sg=np.empty((na,nc),dtype=np.float32) #sigma
lb=np.empty((na,nc),dtype=np.float32) #lower-bound
ub=np.empty((na,nc),dtype=np.float32) #upper-bound
###========================###
### generate mu            ###
###========================###
def genMu(na,nc,span,dist):
    if dist=='u': #uniform distribution of MUs
        return (np.random.rand(na,nc)-0.5)*span
    else:        #gaussian distribution of MUs
        return np.random.randn(na,nc)*span
mu=genMu(na,nc,span,dist)

###========================###
### generate sigma         ###
###========================###
def genSigma(na,nc,cmpr,dist):
    if dist=='u': #uniform distribution of MUs
        return np.abs(np.random.randn(na,nc)/cmpr)
    else:        #gaussian distribution of MUs
        return np.abs(np.random.rand(na,nc)/cmpr)
sg=genSigma(na,nc,cmpr,dist)

###========================###
### generate range         ###
###========================###
def genRange(mu,sigma):
    return mu-3*sigma,mu+3*sigma
lb,ub=genRange(mu,sg)

###========================###
### get attribute range    ###
###========================###
amin=np.min(lb,axis=1)
amax=np.max(ub,axis=1)
sp=open('spec.arff','w')
sp.write("@relation multiple-gaussian ["+str(na)+","+str(nc)+"]\n")
print("================ print spec ================")
for i in range(na):
    arange="\t{"+str(amin[i])+","+str(amax[i])+"}"
    print ("@attribute a"+str(i+1)+arange)
    sp.write("@attribute a"+str(i+1)+arange+"\n")
    for j in range(nc):
        print ("@class{0:d} \t[mu={3:3.5f}, \tsg={4:3.5f}]".format(j+1,lb[i,j],ub[i,j],mu[i,j],sg[i,j]))
        sp.write ("@class{0:d} \t[mu={3:3.5f}, \tsg={4:3.5f}]\n".format(j+1,lb[i,j],ub[i,j],mu[i,j],sg[i,j]))
sp.close()

for i in range(na):
    prtmu,j="",0
    for m in mu[i]:
        prtmu+=str(m)
        if j<nc-1:
            prtmu+=","
        j+=1
    #print (prtmu)
for i in range(na):
    prtsg,j="",0
    for s in sg[i]:
        prtsg+=str(s)
        if j<nc-1:
            prtsg+=","
        j+=1
    #print (prtsg)

cls=""
for i in range(nc):
    cls+=str(i+1)
    if i<nc-1:
        cls+=","

hd=open('head.arff','w')
hd.write("@relation multiple-gaussian \n")
print("================ print head ================")
print("@relation multiple-gaussian")
for i in range(na):
    arange="\t{"+str(amin[i])+","+str(amax[i])+"}"
    hd.write("@attribute a"+str(i+1)+" numeric"+arange+"\n")
    print ("@attribute a"+str(i+1)+" numeric"+arange)
hd.write("@attribute class {"+cls+"} \n")
print("@attribute class {"+cls+"}")
hd.close()
