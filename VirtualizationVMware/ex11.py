from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import time

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Establish a connection to the vCenter server
c = SmartConnect(host="10.1.2.24", user="devops", pwd="Student2021!", port=443)
vm_name = "Roy's First VM"

# content:  object that represents the content of the vCenter server.
content = c.RetrieveContent()

# container view that allows us to retrieve a specific type of object from the vCenter server's inventory
container = content.viewManager.CreateContainerView(
    content.rootFolder, [vim.VirtualMachine], True
    # content.rootFolder: specifies the root folder of the inventory.
    # [vim.VirtualMachine]: specifies the type of objects we want to retrieve, in this case, virtual machines.
    # True:  indicates that the container view should recursively search for objects of the specified type in all subfolders of the root folder.
)



actual_vm = None
for vm in container.view:
    if vm.name == vm_name:
        actual_vm = vm

print(actual_vm.runtime.powerState)
if actual_vm.runtime.powerState == "poweredOff":
    actual_vm.PowerOn
    print(actual_vm.runtime.powerState)


