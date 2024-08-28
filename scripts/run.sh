#!/bin/bash -ex

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

cp -v files/*.json "${ROOTFS_DIR}/var/tmp/"

on_chroot << EOF

apt list --installed > /var/tmp/before-install.list

python -m venv /var/tmp/venv

source /var/tmp/venv/bin/activate

pip install debian-package-installer@git+https://github.com/EffectiveRange/debian-package-installer.git@latest

debian-package-installer.py /var/tmp/package-config.json --source-config /var/tmp/source-config.json

apt list --installed > /var/tmp/after-install.list

touch /etc/first_boot

EOF

cp -v "${ROOTFS_DIR}/var/tmp/before-install.list" "${DEPLOY_DIR}/"
cp -v "${ROOTFS_DIR}/var/tmp/after-install.list" "${DEPLOY_DIR}/"
