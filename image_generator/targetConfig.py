# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from typing import Optional

from package_downloader import PackageConfig
from package_installer import SourceConfig
from pydantic import BaseModel


class TargetConfig(BaseModel):
    name: str
    version: str
    reference: str
    stage: int = 2
    packages: list[PackageConfig]
    sources: Optional[list[SourceConfig]] = None
    boot_cmdline: Optional[list[str]] = None
    boot_config: Optional[list[str]] = None
    first_boot: Optional[list[str]] = None
    pre_install: Optional[list[str]] = None
    post_install: Optional[list[str]] = None
