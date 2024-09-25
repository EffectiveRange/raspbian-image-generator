#!/bin/bash -ex

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

cp -v files/*.json "${ROOTFS_DIR}/var/tmp/"

on_chroot << EOF

cd /var/tmp

apt list --installed > before-install.list

python -m venv venv

venv/bin/pip3 install debian-package-installer@git+https://github.com/EffectiveRange/debian-package-installer.git@latest

venv/bin/debian-package-installer.py package-config.json --source-config source-config.json

apt list --installed > after-install.list

touch /etc/first_boot

EOF

mkdir -p "${DEPLOY_DIR}"
cp -v "${ROOTFS_DIR}/var/tmp/before-install.list" "${DEPLOY_DIR}"
cp -v "${ROOTFS_DIR}/var/tmp/after-install.list" "${DEPLOY_DIR}"
