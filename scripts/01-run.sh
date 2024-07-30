#!/bin/bash -e

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

cp files/*.json "${ROOTFS_DIR}/tmp/"

RELEASE_INFO=$(cat "${ROOTFS_DIR}/etc/os-release")
RELEASE_VERSION=$(echo "${RELEASE_INFO}" | grep VERSION_ID | cut -d '"' -f 2)

on_chroot << EOF

python -m venv /tmp/venv

source /tmp/venv/bin/activate

if [ "${RELEASE_VERSION}" = "11" ]; then
  # Workaround for cryptography 43.0.0 forcing the use of OpenSSL 3 which is not available in Debian 11
  pip install --force-reinstall -v cryptography==42.0.8
fi

pip install debian-package-installer@git+https://github.com/EffectiveRange/debian-package-installer.git@latest

debian-package-installer.py /tmp/package-config.json --source-config /tmp/source-config.json

EOF
