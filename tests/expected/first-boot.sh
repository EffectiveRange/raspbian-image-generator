#!/bin/bash -ex

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

first_boot_file="/etc/first_boot"

echo_serial() {
    echo "$1" >> /dev/serial0
}

first_boot_cleanup() {
    trap - EXIT

    if [ "$2" -ne 0 ]; then
        echo_serial "Failed to run first boot setup: '${1% >> /dev/serial0 2>&1}' returned non-zero exit status $2"
        exit 1
    fi
}

if [ ! -f /dev/serial0 ]; then
    ln -s /dev/ttyAMA0 /dev/serial0
fi

trap 'first_boot_cleanup "$BASH_COMMAND" "$?"' EXIT

if [ -f "$first_boot_file" ]; then
    echo_serial "Removing first boot file $first_boot_file"
    rm -f "$first_boot_file"

    echo_serial "Running first boot setup..."

    echo_serial "Running command: cmd1"
    cmd1 >> /dev/serial0 2>&1
    echo_serial "Command exit code: $?"

    echo_serial "Running command: cmd2"
    cmd2 >> /dev/serial0 2>&1
    echo_serial "Command exit code: $?"

    echo_serial "First boot setup completed."
fi

exit 0
