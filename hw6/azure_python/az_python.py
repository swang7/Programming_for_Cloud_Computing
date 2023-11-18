# Import the needed credential and management objects from the libraries.
import os

from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute.models import DiskCreateOption

RESOURCE_GP = "az-vm-rg"
LOCATION = "westus3"
VM_NAME = "ucscx-homework-6-problem-2"
VM_SIZE = "Standard_B1s"
ADM_USERNAME = "ucscxuser"
PASSWORD = "Pw_Az2023"
DISK_NAME = "Homework-6.2"
DISK_NAME_P1 = "Homework-6.1"
SNAPSHOT_NAME = "Homework-6.1-snapshot"

print("Provisioning a virtual machine...some operations might take a minute or two.")

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]


# Step 1: resource group

# Obtain the management object for resources, using the credentials
# from the CLI login.
resource_client = ResourceManagementClient(credential, subscription_id)

# Provision the resource group.
rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GP,
   {
       "location": LOCATION
   }
)

print(f"1. Provisioned resource group {rg_result.name} in the {rg_result.location} region")

# # Get the resource group.
# rg_result = resource_client.resource_groups.get(RESOURCE_GP)

# print(f"Got resource group {rg_result.name} in the {rg_result.location} region")

# Step 2: provision a virtual network

# A virtual machine requires a network interface client (NIC). A NIC
# requires a virtual network and subnet along with an IP address.
# Therefore we must provision these downstream components first, then
# provision the NIC, after which we can provision the VM.

# Network and IP address names
VNET_NAME = "az-hw6p2-vnet"
SUBNET_NAME = "az-hw6p2-subnet"
IP_NAME = "az-hw6p2-ip"
IP_CONFIG_NAME = "az-hw6p2-ip-config"
NIC_NAME = "az-hw6p2-nic"
NETWORK_SECURITY_GROUP = "az-hw6p2-nsg"
SECURITY_RULE = "allow-ssh"

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

# Provision the virtual network and wait for completion
poller = network_client.virtual_networks.begin_create_or_update(
    RESOURCE_GP,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {"address_prefixes": ["10.0.0.0/16"]},
    },
)

vnet_result = poller.result()

print(f"2. Provisioned virtual network {vnet_result.name} with address \
prefixes {vnet_result.address_space.address_prefixes}"
)

# Step 3: Provision the subnet and wait for completion
poller = network_client.subnets.begin_create_or_update(
    RESOURCE_GP,
    VNET_NAME,
    SUBNET_NAME,
    {"address_prefix": "10.0.0.0/24"},
)
subnet_result = poller.result()

print(f"3. Provisioned virtual subnet {subnet_result.name} with address \
prefix {subnet_result.address_prefix}"
)

# Step 4: Provision an IP address and wait for completion
poller = network_client.public_ip_addresses.begin_create_or_update(
    RESOURCE_GP,
    IP_NAME,
    {
        "location": LOCATION,
        "sku": {"name": "Standard"},
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4",
    },
)

ip_address_result = poller.result()

print(f"4. Provisioned public IP address {ip_address_result.name} \
with address {ip_address_result.ip_address}")

# Create network security group
nsg_result = network_client.network_security_groups.begin_create_or_update(
    RESOURCE_GP,
    NETWORK_SECURITY_GROUP,
    {
        "location": LOCATION
    }
).result()
print(f"5. Create network security group: {nsg_result.name}")

# Create security rule
security_rule = network_client.security_rules.begin_create_or_update(
    RESOURCE_GP,
    NETWORK_SECURITY_GROUP,
    SECURITY_RULE,
    {
        "protocol": "TCP",
        "source_address_prefix": "*",
        "destination_address_prefix": "*",
        "access": "Allow",
        "destination_port_range": "22",
        "source_port_range": "*",
        "priority": "100",
        "direction": "Inbound"
    }
).result()
print(f"5.1 Create security rule: {security_rule.name}")

# Step 6: Provision the network interface client
poller = network_client.network_interfaces.begin_create_or_update(
    RESOURCE_GP,
    NIC_NAME,
    {
        "location": LOCATION,
        "ip_configurations": [
            {
                "name": IP_CONFIG_NAME,
                "subnet": {"id": subnet_result.id},
                "public_ip_address": {"id": ip_address_result.id},
            }
        ],
        "network_security_group": {
            "id": nsg_result.id,
        }
    },
)

nic_result = poller.result()

print(f"6. Provisioned network interface client {nic_result.name}")

# Obtain the compute management object
compute_client = ComputeManagementClient(credential, subscription_id)

# get snapshot
p1_snapshot = compute_client.snapshots.get(RESOURCE_GP, SNAPSHOT_NAME)

poller = compute_client.disks.begin_create_or_update(
    RESOURCE_GP,
    DISK_NAME,
    {
        'location': LOCATION,
        'sku': {"name": "StandardSSD_LRS"},
        'disk_size_gb': 1,
        'tags' : {
            'Homework': '6.2'
        },
        'creation_data': {
            'create_option': DiskCreateOption.Copy,
            'source_resource_id': p1_snapshot.id,
        }
    }
)
disk_resource = poller.result()

print(f"7. Created disk {disk_resource.name}")

p1_disk = compute_client.disks.get(RESOURCE_GP, DISK_NAME_P1)
print(f"7.1 Got old disk from problem 1 {p1_disk.name}")

# Step 8: Provision the virtual machine
print(f"\nProvisioning virtual machine {VM_NAME}; this operation might \
take a few minutes.")

# Provision the VM specifying only minimal arguments, which defaults
# to an Ubuntu 18.04 VM on a Standard DS1 v2 plan with a public IP address
# and a default virtual network/subnet.

poller = compute_client.virtual_machines.begin_create_or_update(
    RESOURCE_GP,
    VM_NAME,
    {
        "location": LOCATION,
        "tags": {
            'Homework': 'ucscx-homework-6-problem-2'
        },
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "0001-com-ubuntu-server-jammy",
                "sku": "22_04-lts-gen2",
                "version": "latest",
            }
        },
        "hardware_profile": {"vm_size": VM_SIZE},
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": ADM_USERNAME,
            "admin_password": PASSWORD,
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": nic_result.id,
                }
            ]
        },
    },
)

vm_result = poller.result()

print(f"8. Provisioned virtual machine {vm_result.name}")

poller = compute_client.virtual_machines.begin_update(
    RESOURCE_GP,
    VM_NAME,
    {
        "storage_profile" : {
            "data_disks" : [
                {
                    'lun': 0,
                    'create_option': DiskCreateOption.attach,
                    'managed_disk': {
                        'id': disk_resource.id,
                    }
                },
                {
                    'lun': 1,
                    'create_option': DiskCreateOption.attach,
                    'name': DISK_NAME_P1,
                    'managed_disk': {
                        'id': p1_disk.id,
                    }
                }
            ]
        }
    }
)

disk_attach_result = poller.result()

print(f"9. Attached disk {disk_resource.name} and {DISK_NAME_P1} to vm {vm_result.name}\n")

answer = input("Shutdown the VM and clean up (yes/no): ")

if answer != "yes":
    exit(0)

# stop the VM
compute_client.virtual_machines.begin_power_off(RESOURCE_GP, VM_NAME).result()
print(f"VM {VM_NAME} shutdown")

# detach the disk
virtual_machine = compute_client.virtual_machines.get(RESOURCE_GP, VM_NAME)

data_disks = virtual_machine.storage_profile.data_disks
data_disks.clear()
compute_client.virtual_machines.begin_update(RESOURCE_GP, VM_NAME, virtual_machine)
print(f"VM {VM_NAME}, data disk detached")

# terminate the VM
compute_client.virtual_machines.begin_deallocate(RESOURCE_GP, VM_NAME).result()
print(f"VM {VM_NAME} terminated")

# delete disks
compute_client.disks.begin_delete(RESOURCE_GP, DISK_NAME)
compute_client.disks.begin_delete(RESOURCE_GP, DISK_NAME_P1)
print(f"Disks {DISK_NAME} and {DISK_NAME_P1} destroyed")