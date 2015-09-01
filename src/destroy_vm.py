import libvirt
import create_vm
import get
import start
import os

def destroy(vid):
	fopen =open("virinfo","r")
	lines =fopen.readlines()
	fopen.close()
	cnt=0
	myname=0
	fopen1 =open("virinfo1","w")
	words1=[]
	for line in lines:
		words1=line.split(" ")
		if str(words1[0])!=str(vid):
			fopen1.write(str(words1[0])+" "+str(words1[1])+" "+str(words1[2])+" "+str(words1[3]))
		else:
			myname = words1[1]
		cnt=cnt+1
	fopen1.close()
	fopen1=open("virinfo1","r")
	lines =fopen1.readlines()
	fopen1.close()
	fopen2=open("virinfo","w")
	for x in lines:
		fopen2.write(x)
	connect = libvirt.open("remote+ssh://"+create_vm.pmList[int(create_vm.pm_n)].strip('\n')+"/")
	req = connect.lookupByName(str(myname))
	if req.isActive():
		req.destroy()
	req.undefine()
	return {"status":"1"}