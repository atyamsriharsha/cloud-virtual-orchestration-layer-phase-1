import libvirt
import create_vm
import get
import start
def query(vid):
	mydict={}
	fopen12 = open("virinfo","r")
	lines12=fopen12.readlines()
	fopen12.close()
	for line in lines12:
		if line[:4]==str(vid):
			words=line.split(" ")
			mydict['vmID']=words[0]
			mydict['name']=words[1]
			mydict['instance_type']=words[2]
			mydict['pmID']=words[3]
			break
	return mydict
	'''
	try:
		for i in create_vm.vmList:
			if i[0]==vid:
				mydict['vmID']=i[0]
				mydict['name']=i[1]
				mydict['instance_type']=i[2]
				mydict['pmID']=i[3]
				break
		return mydict
	except:
		return mydict
	'''