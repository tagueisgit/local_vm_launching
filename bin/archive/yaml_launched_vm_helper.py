import os
import time

IMAGES_DIR = "/data/VMs/debian/"
BACKING_IMAGE = "debian-backing-image.qcow2"

time.sleep(2)  # Sleep for 2 seconds

def get_shutoff_vms():
    result = os.popen("virsh list --all | grep 'shut off'").read().splitlines()
    return [line.split()[1] for line in result]

def remove_all_except_backing_image():
    for file_name in os.listdir(IMAGES_DIR):
        if file_name.endswith('.qcow2') and file_name != BACKING_IMAGE:
            print("Removing file_name")
            os.remove(os.path.join(IMAGES_DIR, file_name))

loop_count = 0  # Initialize the loop counter

while loop_count < 3:  # Loop only 3 times
    shut_off_vms = get_shutoff_vms()

    if not shut_off_vms:
        all_vms = os.popen("virsh list --all").read()
        if not all_vms.strip():  # Check if the output is empty
            remove_all_except_backing_image()
            print("All .qcow2 files except for the backing image have been removed.")
            break  # Exit the loop after removing files

    for vm in shut_off_vms:
        # Delete the disk image
        image_path = os.path.join(IMAGES_DIR, f"{vm}.qcow2")
        if os.path.exists(image_path) and f"{vm}.qcow2" != BACKING_IMAGE:
            os.remove(image_path)
            os.system(f"virsh undefine {vm}")  # Destroy the VM definition
            print(f"Cleaned up VM {vm}")

    time.sleep(10)  # Check every 10 seconds
    loop_count += 1  # Increment the loop counter

