###================================###
### gaussian data generator
### output: head.arff
### pars na: number of attributes
###      nc: number of classes
###================================###
import numpy as np
import sys

if len(sys.argv)==3:
    na=int(sys.argv[1])
    nc=int(sys.argv[2])
else:
    print "python headergen.py $max_att $max_cls"
    exit()
print ("num_attr(%d) num_class(%d)" % (na, nc))

cls=""
for i in range(nc):
    cls+=str(i+1)
    if i<nc-1:
        cls+=","
###========================###
### write to head.arff     ###
###========================###
hd=open('head.arff','w')
hd.write("@relation multiple-gaussian \n")
print("@relation multiple-gaussian")
for i in range(na):
    hd.write("@attribute a"+str(i+1)+" numeric \n")
    print ("@attribute a"+str(i+1)+" numeric")
hd.write("@attribute class {"+cls+"} \n")
print("@attribute class {"+cls+"}")
hd.close()
