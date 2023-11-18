#!/bin/bash
set -o errexit; set -o pipefail; set -o nounset

RESOURCE_GP=az-vm-rg
LOCATION=westus3
VM_NAME=ucscx-homework-6-part-1
VM_IMAGE=Ubuntu2204
VM_SIZE=Standard_B1s
ADM_USERNAE=ucscxuser
DISK_NAME=Homework-6.1

echo "create resoure group..."
az group create --name "$RESOURCE_GP" --location "$LOCATION"

echo "create VM..."
az vm create \
    --resource-group $RESOURCE_GP \
    --name $VM_NAME \
    --image $VM_IMAGE \
    --size $VM_SIZE \
    --tags Homework=ucscx-homework-6-part-1 \
    --admin-username $ADM_USERNAE \
    --security-type 'Standard' \
    --generate-ssh-keys \
    --public-ip-sku Standard \
    --output json \
    --verbose

echo "create disk..."
az disk create \
    --resource-group $RESOURCE_GP \
    --name $DISK_NAME \
    --size-gb 1 \
    --sku Standard_LRS \
    --tags Homework=6.1

echo "attach disk..."
az vm disk attach \
    --resource-group $RESOURCE_GP \
    --vm-name $VM_NAME \
    --name $DISK_NAME

echo "VM is ready"
read -r -p "Press Enter to shutdown VM" < /dev/tty

az vm stop --resource-group $RESOURCE_GP --name $VM_NAME

echo "detach the disk..."
az vm disk detach --resource-group $RESOURCE_GP --vm-name $VM_NAME --name $DISK_NAME

echo "deallocate vm..."
az vm deallocate --resource-group $RESOURCE_GP --name $VM_NAME