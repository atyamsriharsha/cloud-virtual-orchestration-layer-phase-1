import libvirt
import os
import get
import start
from random import randint
from uuid import uuid4
import subprocess
import os
import json

pmID=0
vmID=0
ImgList=[]
vmList=[]
pmList=[]
pm_n=0
pwf =open("machines","r")
lines1 =pwf.readlines()
for line1 in lines1:
	pmList.append(str(line1.strip('\n')))

pwf1 =open("Images","r")
lines2=pwf1.readlines()
for line2 in lines2:
	ImgList.append(str(line2.strip('\n')))

print ImgList

def create(attrs):
	global pmID,vmID,vmList,ImgList
	global pm_n
	name=attrs["name"]
	instance_type = int(attrs["instance_type"])
	file_data = open("Vm_types","r")
	json_data = json.load(file_data)
	cpu = json_data['types'][instance_type-1]['cpu'] 
	ram = json_data['types'][instance_type-1]['ram'] 
	disk = json_data['types'][instance_type-1]['disk']
	image_id=attrs["image_id"]
	Image_name = image_id + ".img"
	uid = str(uuid4())
	os.system(" ssh " + pmList[pm_n] +" free -k | grep 'Mem:' | awk '{ print $4 }' >> data12_pm") 
	os.system(" ssh " + pmList[pm_n] +" grep processor /proc/cpuinfo | wc -l >> data12_pm")
	file_data = open("data1_pm", "r") 
	pm_ram = file_data.readline().strip("\n") 
	pm_cpu = file_data.readline().strip("\n")
	vmID=randint(1001,9999)
	while int(pm_ram)>=int(ram) and int(pm_cpu)>=int(cpu):
		pm_n = pm_n + 1
		if pm_n == len(pmList):
			return jsonify(status=0)
		os.system(" ssh " + create_vm.pmList[create_vm.pm_n] +" free -k | grep 'Mem:' | awk '{ print $4 }' >> data12_pm") 
		os.system(" ssh " + create_vm.pmList[create_vm.pm_n] +" grep processor /proc/cpuinfo | wc -l >> data12_pm")
		file_data = open("data1_pm", "r") 
		pm_ram = file_data.readline().strip("\n") 
		pm_cpu = file_data.readline().strip("\n")
	fopen = open("virinfo","a")
	fopen1 =open("virinfo1","a")
	fopen1.write(str(vmID)+" "+str(name)+" "+str(instance_type)+" "+str(pm_n)+"\n")
	fopen1.close()
	fopen.write(str(vmID)+" "+str(name)+" "+str(instance_type)+" "+str(pm_n)+"\n")
	fopen.close()
	frt = open("pm_file","a")
	frt.write(str(pmID))
	frt.close()
	send_image(pmList[int(pm_n)],ImgList[int(image_id)-1].split(":")[1])
	image_path = "/home/"+pmList[pm_n].split("@")[0]+"/"+ImgList[int(image_id)-1].split("/")[-1]
	print image_path
	connect = libvirt.open("remote+ssh://"+pmList[int(pm_n)].strip('\n')+"/")
	xml="""<domain type='qemu' id='"""+uid+"""'>
			  <name>"""+name+"""</name>
		  <memory unit='KiB'>"""+str(instance_type)+"""</memory>
		  <vcpu placement='static'>1</vcpu>
		  <os>
		    <type arch='x86_64' machine='pc-0.11'>hvm</type>
		  </os>
		  <devices>
		    <disk type='file' device='cdrom'>
		      <source file='"""+str(image_path) +"""'/>
		      <target dev='hdc' bus='ide'/>
		    </disk>
		  </devices>
		</domain>
 		"""
	req = connect.defineXML(xml)
#	try:
	req.create()
	return {"vmID": vmID}
#	except:
#		return {"vmID" : 0 }

def send_image(pm, image_path):
	image_path = image_path.strip("\r")
	bash_command = "scp " + image_path + " " + pm + ":/home/" + pm.split("@")[0] + "/"
	os.system(bash_command)

def vm_type():
	return get.Desc

def image_list():
	print_imglist = []
	for i in get.image_list:
		mydict = {}
		mydict['id'] = i[0]
		mydict['name'] = i[1].split('.')[0]
		print_imglist.append(mydict)
	return {"Images" : print_imglist }
