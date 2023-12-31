#!/bin/bash

BACKING_IMAGE_PATH="/data/VMs/fedora_coreos/fedora_coreos_backing_image.qcow2"
VM_NAME="fedora_coreos_backing_image"
RAM="4096"
VCPUS="2"
OS_VARIANT="fedora-coreos-stable"

# Check if VM is already defined
VM_EXISTS=$(virsh list --all | grep $VM_NAME)

if [ -z "$VM_EXISTS" ]; then
    # If VM is not defined, define it and start it
    virt-install \
        --name=$VM_NAME \
        --memory=$RAM \
        --vcpus=$VCPUS \
        --disk path=$BACKING_IMAGE_PATH \
        --os-variant=$OS_VARIANT \
        --import
else
    # If VM is already defined, just start it
    virsh start $VM_NAME
    sleep 4
    virt-viewer $VM_NAME
fi
