#!/bin/bash -ex

# Define the FIRST_BOOT variable
FIRST_BOOT=1

# Check if FIRST_BOOT equals 1
if [ "$FIRST_BOOT" -eq 1 ]; then
    echo "Running first boot setup..."

    cmd1
    cmd2

    # Modify this script to set FIRST_BOOT to 0
    sed -i 's/FIRST_BOOT=1/FIRST_BOOT=0/' "$0"

    echo "First boot setup completed."
fi

exit 0
