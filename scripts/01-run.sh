#!/bin/bash -e

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

cp files/*.json "${ROOTFS_DIR}/tmp/"

on_chroot << EOF

python -m venv /tmp/venv

source /tmp/venv/bin/activate

pip install debian-package-installer@git+https://github.com/EffectiveRange/debian-package-installer.git@latest

debian-package-installer.py /tmp/package-config.json --source-config /tmp/source-config.json

EOF
