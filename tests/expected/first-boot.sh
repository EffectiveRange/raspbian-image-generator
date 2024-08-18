#!/bin/bash -ex

FIRSTBOOT="/usr/lib/raspberrypi-sys-mods/firstboot"

sed -i '/^reboot_pi$/i cmd1 "test1"' "$FIRSTBOOT"
sed -i '/^reboot_pi$/i cmd2 '\''test2'\''' "$FIRSTBOOT"
sed -i '/^reboot_pi$/i \\' "$FIRSTBOOT"
