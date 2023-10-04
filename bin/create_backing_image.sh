#!/bin/bash

# Prompting the user for VM details
read -p "Enter the VM name: " VM_NAME
read -p "Enter the memory size (e.g., 2048 for 2GB): " RAM
read -p "Enter the number of vCPUs: " VCPUS
read -p "Enter the disk path (e.g., /path/to/disk.qcow2): " DISK_PATH

# Check if the disk image already exists
if [[ ! -f $DISK_PATH ]]; then
    read -p "Disk image not found. Enter the size of the new disk in gigabytes (e.g., 10 for 10GB): " DISK_SIZE
fi

read -p "Enter the os-variant (e.g., ubuntu20.04): " OS_VARIANT
read -p "Enter the path to the installation media (e.g., /path/to/ubuntu.iso): " CDROM

# Check if VM is already defined
VM_EXISTS=$(virsh list --all | grep $VM_NAME)

if [ -z "$VM_EXISTS" ]; then
    # If VM is not defined, define it and start it
    if [[ -n $DISK_SIZE ]]; then
        virt-install \
            --name=$VM_NAME \
            --memory=$RAM \
            --vcpus=$VCPUS \
            --disk path=$DISK_PATH,size=$DISK_SIZE \
            --cdrom=$CDROM \
            --os-variant=$OS_VARIANT \
            --graphics spice
    else
        virt-install \
            --name=$VM_NAME \
            --memory=$RAM \
            --vcpus=$VCPUS \
            --disk path=$DISK_PATH \
            --cdrom=$CDROM \
            --os-variant=$OS_VARIANT \
            --graphics spice
    fi
else
    # If VM is already defined, just start it
    virsh start $VM_NAME
fi

# Wait a bit for VM to start
sleep 10

# Connecting to the VM using virt-viewer
echo "Connecting to $VM_NAME using virt-viewer..."
virt-viewer -c qemu:///system $VM_NAME

