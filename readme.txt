Cloud orchestrartion Layer:
A cloud orchestration Layer creating,querying,deleting and scheduling Virtual machines in a given network

Vm_create:
url:http://127.0.0.1:5000/server/vm/create/?name=Vm_name&instance_type=instance_type&image_id=image_id
The user can request the flavour and should give three arguments Vm_name ,instancetypea and imgid and the create_vm file creates the necesssary environment if it is able to create and returns the vmid of the virtual machine

Vm_query:
url:http://127.0.0.1:5000/server/vm/query?Vmid=Vmid
If the user want to query about a particular vm the user should give a single argument which is the vmid of the machine

Vm_destroy:
http://127.0.0.1:5000/server/vm/destroy?vmid=vmid
If the user want to delete the particular vm then he should give a single argument which is vmid of the machine

Vm_types:
http://127.0.0.1:5000/server/vm/types
if the user wants to see all the vm's created that are running currently


virinfo contains all the vmid's running currently that is which are not destroyed
