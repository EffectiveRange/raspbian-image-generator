#!/bin/bash -ex

first_boot_file="/etc/first_boot"

trap 'echo "Failed to run first boot setup!" >> /dev/serial0' EXIT

# Check if /etc/first_boot exists
if [ -f "$first_boot_file" ]; then

    # remove /etc/first_boot
    rm -f "$first_boot_file"
    echo "Removing first boot file before setup" >> /dev/serial0

    echo "Running first boot setup..." >> /dev/serial0

    cmd1
    cmd2

    echo "First boot setup completed." >> /dev/serial0
fi

exit 0

trap - EXIT

# remove /etc/first_boot if setup failed
rm -f "$first_boot_file"
echo "Removing first boot file after failure" >> /dev/serial0

exit 1
