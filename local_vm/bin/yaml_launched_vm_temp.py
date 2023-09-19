#!/usr/bin/env python3

import yaml
import os
import argparse
import logging
import subprocess
import sys
import time
import signal

logging.basicConfig(filename='log/vm_creation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def signal_handler(signum, frame):
    print("You pressed Ctrl + C!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def monitor_vm_shutdown(domain_name):
    print(f"Monitoring {domain_name} for shut off event...")
    
    while True:
        # Check if VM exists
        vm_status = os.popen(f"sudo virsh list --all | grep -w {domain_name}").read().strip()
        if not vm_status:
            # VM no longer exists, cleanup and exit
            cleanup_vm(domain_name)
            print(f"{domain_name} has been shut off. Image cleaned up. Exiting script.")
            sys.exit(0)  
        time.sleep(2)  # Wait for a short duration before rechecking

def cleanup_vm(vm_name):
    # This function cleans up the VM after it's shut off

    image_path = os.path.join("/data/VMs/debian", "debian_vm_test.qcow2")
    if os.path.exists(image_path):
        os.system(f"sudo rm {image_path}")
        logging.info(f"Cleaned up VM image: {image_path}")
    else:
        logging.warning(f"Disk image {image_path} does not exist. Skipping image cleanup.")

def create_vm_from_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error reading configuration: {e}")
        return

    try:
        cmd = f"virt-install --name={config['vm']['name']} --memory={config['vm']['memory']} --vcpus={config['vm']['cpus']} --os-variant={config['vm']['os_variant']} --import"
        
        if 'cdrom' in config['vm']:
            cmd += f" --cdrom={config['vm']['cdrom']}"

        if config['vm'].get('transient', False):
            cmd += " --transient"

        if 'backing_image' in config['vm']['disk']:
            overlay_image_path = config['vm']['disk']['path']
            cmd_create_overlay = f"qemu-img create -f qcow2 -b {config['vm']['disk']['backing_image']} -F qcow2 {overlay_image_path}"
            os.system(cmd_create_overlay)

        cmd += f" --disk path={config['vm']['disk']['path']},size={config['vm']['disk']['size']}"

    except KeyError as e:
        logging.error(f"KeyError in configuration: {e}")
        return

    exit_code = os.system(cmd)
    if exit_code != 0:
        logging.error(f"'virt-install' command exited with code {exit_code}.")
    else:
        logging.info(f"'virt-install' command executed successfully for {config['vm']['name']}.")

    # After the VM is created
    monitor_vm_shutdown(config['vm']['name'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a VM based on a YAML configuration.')
    parser.add_argument('config_path', type=str, help='Path to the YAML configuration file.')
    args = parser.parse_args()
    logging.info(f"Starting VM creation from {args.config_path}.")
    create_vm_from_config(args.config_path)
    logging.info(f"Finished VM creation process for {args.config_path}.")

