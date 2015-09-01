#!/usr/bin/env python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import sys
import os
import create_vm
import get
import destroy_vm
import query_vm
import libvirt
app = Flask(__name__)

@app.route('/server/vm/create/' , methods = ['GET'])
def request_create():
	vm={}
	vm['name']=request.args.get('name')
	vm['instance_type']=request.args.get('instance_type')
	vm['image_id']=request.args.get('image_id')
	return jsonify(create_vm.create(vm))

@app.route('/server/vm/destroy/' , methods = ['GET'])
def request_destroy():
	vmID=request.args.get('vmID')
	#print int(vmID)
	#return str(destroy_vm.destroy(int(vmID)))
	return jsonify(destroy_vm.destroy(int(vmID)))

@app.route('/server/vm/query/' , methods = ['GET'])
def request_query():
	vmID=request.args.get('vmID')
	return jsonify(query_vm.query(int(vmID)))

@app.route('/server/vm/types/')
def request_types():
	return jsonify(create_vm.vm_type())

@app.route('/server/vm/image/list')
def request_imagelist():
	return jsonify(create_vm.image_list())

@app.route('/server/pm/list')
def request_pm():
	fileopen = open("machines","r")
	fileinfo = fileopen.readlines()
	count = 0	
	L = []
	for i in fileinfo:
		count = count +1 
		L.append(count)
	fileopen.close()	
	return jsonify(pmids = L) 

connect = ""

@app.route('/server/pm/query')
def request_pmquery():
	global connect
	list12 =[]
	list22=[]
	pmid=request.args.get('pmid')
	pmid=str(pmid)
	connect = libvirt.open("remote+ssh://"+create_vm.pmList[int(pmid)].strip('\n')+"/")
	os.system(" ssh " + create_vm.pmList[create_vm.pm_n] +" free -k | grep 'Mem:' | awk '{ print $4 }' >> data1_pm") 
	os.system(" ssh " + create_vm.pmList[create_vm.pm_n] +" grep processor /proc/cpuinfo | wc -l >> data1_pm")
	file_data = open("data1_pm", "r") 
	pm_ram = file_data.readline().strip("\n") 
	pm_cpu = file_data.readline().strip("\n")
	list12.append(pm_ram)
	list12.append(pm_cpu)
	os.system("rm -rf data_pm") 
	'''bits = 32 
	try: 
		os.system("ssh " + pmList[pm_n] + " cat /proc/cpuinfo | grep lm ") 
		bits = '64' 
	except: 
		bits = '32' 
	substring = "64" 
	if substring in image_path:
		image_bit = 64 
	else: 
		image_bit = 32
	''' 
	return jsonify(capacity=list12)

@app.route('/server/pm/listvms')
def request_listvm():
	pmid = request.args.get('pmid')
	pmid = str(pmid)
	fileopen = open("virinfo1" , "r")
	vms_present = []	
	for i in fileopen:		
		curr_vm = i.split()
		if curr_vm[3] == pmid:
			vms_present.append(int(curr_vm[0]))
	return jsonify(vmids = vms_present)	


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
	get.create_machines(sys.argv[1])
	get.create_images(sys.argv[2])
	get.CreateTypes(sys.argv[3])
   	app.run(debug = True)
