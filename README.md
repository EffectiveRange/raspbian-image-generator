# raspbian-image-generator

Raspberry Pi OS image generator using the official pi-gen repository

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
    - [Install from source root directory](#install-from-source-root-directory)
    - [Install from source distribution](#install-from-source-distribution)
- [Usage](#usage)
    - [Command line reference](#command-line-reference)
    - [Example](#example)

## Features

- [x] Generate Raspberry Pi OS images
- [x] Install additional packages into the image
- [x] Customize boot options (cmdline.txt, config.txt)
- [x] Run custom commands before and/or after installing the packages

## Requirements

- [Python3](https://www.python.org/downloads/)
- [GitPython](https://gitpython.readthedocs.io/en/stable/)
- [jinja2](https://jinja.palletsprojects.com/)
- [pydantic](https://docs.pydantic.dev/latest/#pydantic-examples)

## Installation

### Install from source root directory

```bash
pip install .
```

### Install from source distribution

1. Create source distribution
    ```bash
    python setup.py sdist
    ```

2. Install from distribution file
    ```bash
    pip install dist/raspbian-image-generator-1.0.0.tar.gz
    ```

3. Install from GitHub repository
    ```bash
    pip install git+https://github.com/EffectiveRange/raspbian-image-generator.git@latest
    ```

## Usage

### Command line reference

```commandline
usage: raspbian-image-generator.py [-h] [-f LOG_FILE] [-l LOG_LEVEL] [-d DOWNLOAD] [-p REPOSITORY_PATH] [-u REPOSITORY_URL] [-o OUTPUT] [-t CONFIG_TEMPLATE] [-c COMPRESSION] [--enable-ssh | --no-enable-ssh] [--clean-build | --no-clean-build] target_config target_name

positional arguments:
  target_config         target config JSON file or URL
  target_name           image target config name

options:
  -h, --help            show this help message and exit
  -f LOG_FILE, --log-file LOG_FILE
                        log file path (default: None)
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        logging level (default: INFO)
  -d DOWNLOAD, --download DOWNLOAD
                        target config download location (default: /tmp/config)
  -p REPOSITORY_PATH, --repository-path REPOSITORY_PATH
                        repository location path (default: /tmp/pi-gen)
  -u REPOSITORY_URL, --repository-url REPOSITORY_URL
                        repository URL (default: https://github.com/RPi-Distro/pi-gen.git)
  -o OUTPUT, --output OUTPUT
                        output image directory (default: image)
  -t CONFIG_TEMPLATE, --config-template CONFIG_TEMPLATE
                        pi-gen config template (default: config/config.template)
  -c COMPRESSION, --compression COMPRESSION
                        output image compression (default: xz)
  --enable-ssh, --no-enable-ssh
                        enable SSH access (default: True)
  --clean-build, --no-clean-build
                        clean before build (default: True)
```

### Example

Needs root privileges!

```commandline
$ sudo bin/raspbian-image-generator.py edge-pi-zero -t ~/config/target-config.json
```

Example configuration (example `target-config.json` config file content):

```json
[
  {
    "name": "edge-pi-zero",
    "version": "0.2.1",
    "reference": "2024-03-12-raspios-bullseye",
    "sources": [
      {
        "name": "effective-range",
        "source": "deb http://aptrepo.effective-range.com stable main",
        "key_id": "C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3",
        "key_file": "http://aptrepo.effective-range.com/dists/stable/public.key",
        "key_server": "keyserver.ubuntu.com"
      }
    ],
    "packages": [
      {
        "package": "wifi-manager",
        "release": {
          "owner": "EffectiveRange",
          "repo": "wifi-manager",
          "tag": "latest",
          "matcher": "*armhf.deb"
        }
      },
      {
        "package": "picprogrammer",
        "release": {
          "owner": "EffectiveRange",
          "repo": "pic18-q20-programmer",
          "tag": "v0.3.0",
          "matcher": "*armhf.deb"
        }
      },
      {
        "package": "filebeat",
        "version": "8.12.2",
        "file_url": "https://github.com/EffectiveRange/elastic-beats-armhf-deb/releases/download/v8.12.2/filebeat-8.12.2-armv7l.deb"
      }
    ],
    "boot_cmdline": [
      "modules-load=dwc2,g_ether"
    ],
    "boot_config": [
      "enable_uart=1",
      "dtoverlay=dwc2"
    ],
    "pre_install": [
      "echo 'Pre-install script'"
    ],
    "post_install": [
      "echo 'Post-install script'"
    ]
  }
]
```

Output:

```commandline
2024-07-04T10:32:52.190664Z [info     ] Started image generation       [ImageGeneratorApp] app_version=0.1.0 application=raspbian-image-generator arguments={'log_file': None, 'log_level': 'INFO', 'download': '/tmp/config', 'repository_path': '/tmp/pi-gen', 'repository_url': 'https://github.com/RPi-Distro/pi-gen.git', 'output': 'images', 'config_template': 'config/config.template', 'compression': 'xz', 'enable_ssh': True, 'clean_build': False, 'target_config': 'build/target-config.json', 'target_name': 'edge-pi-zero'} hostname=Legion7iPro target=edge-pi-zero
2024-07-04T10:32:52.191064Z [info     ] Cleaning existing repository   [ImageGeneratorApp] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro path=/tmp/pi-gen repository=https://github.com/RPi-Distro/pi-gen.git
2024-07-04T10:32:52.194713Z [info     ] Local file path provided, skipping download [FileDownloader] app_version=0.1.0 application=raspbian-image-generator file=/home/attilagombos/EffectiveRange/raspbian-image-generator/build/target-config.json hostname=Legion7iPro
2024-07-04T10:32:52.281235Z [info     ] Loading target configuration   [ImageGenerator] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro target=edge-pi-zero
2024-07-04T10:32:52.283144Z [info     ] Checking out reference         [BuildInitializer] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro reference=2024-03-12-raspios-bullseye
2024-07-04T10:32:52.284736Z [info     ] Installing build dependency    [BuildInitializer] app_version=0.1.0 application=raspbian-image-generator dependency=quilt hostname=Legion7iPro
2024-07-04T10:32:52.285036Z [info     ] Package is already installed   [AptInstaller] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro package=quilt version=0.67+really0.66-1
2024-07-04T10:32:52.285319Z [info     ] Dependency installed           [BuildInitializer] app_version=0.1.0 application=raspbian-image-generator dependency=quilt hostname=Legion7iPro
...
2024-07-04T10:32:52.294818Z [info     ] Configuring build              [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro
2024-07-04T10:32:52.294961Z [info     ] Appending boot command line options [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator file=/tmp/pi-gen/stage1/00-boot-files/files/cmdline.txt hostname=Legion7iPro options=['modules-load=dwc2,g_ether']
2024-07-04T10:32:52.295292Z [info     ] Appending boot config options  [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator file=/tmp/pi-gen/stage1/00-boot-files/files/config.txt hostname=Legion7iPro options=['enable_uart=1', 'dtoverlay=dwc2']
2024-07-04T10:32:52.295527Z [info     ] Creating sub-stage             [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro stage=stage2 sub_stage=/home/attilagombos/EffectiveRange/raspbian-image-generator/build/install-packages
2024-07-04T10:32:52.295707Z [info     ] Creating source config file    [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator file=/home/attilagombos/EffectiveRange/raspbian-image-generator/build/install-packages/files/source-config.json hostname=Legion7iPro
2024-07-04T10:32:52.296189Z [info     ] Creating package config file   [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator file=/home/attilagombos/EffectiveRange/raspbian-image-generator/build/install-packages/files/package-config.json hostname=Legion7iPro
2024-07-04T10:32:52.296513Z [info     ] Copying sub-stage scripts      [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro scripts=['00-packages', '01-run.sh']
2024-07-04T10:32:52.297073Z [info     ] Appending sub-stage to stage   [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro stage=stage2 sub_stage=/tmp/pi-gen/stage2/04-install-packages
2024-07-04T10:32:52.298790Z [info     ] Creating build config file     [BuildConfigurator] app_version=0.1.0 application=raspbian-image-generator file=/tmp/pi-gen/config hostname=Legion7iPro
2024-07-04T10:32:52.299196Z [info     ] Building image                 [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator command=./build.sh hostname=Legion7iPro path=/tmp/pi-gen
2024-07-04T10:32:52.299408Z [info     ] Executing command              [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator command=./build.sh hostname=Legion7iPro
2024-07-04T10:32:52.307131Z [info     ] [12:32:52] Begin /tmp/pi-gen   [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro
...
2024-07-04T10:34:20.461214Z [info     ] [12:34:20] Begin /tmp/pi-gen/stage2/04-install-packages/01-run.sh [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro
2024-07-04T10:38:10.770999Z [info     ] Starting package installer     [PackageInstallerApp] app_version=1.0.1 application=debian-package-installer arguments={'log_file': None, 'log_level': 'info', 'source_config': '/tmp/source-config.json', 'download': '/tmp/packages', 'package_config': '/tmp/package-config.json'} hostname=Legion7iPro
2024-07-04T10:38:10.776140Z [info     ] Local file path provided, skipping download [FileDownloader] app_version=1.0.1 application=debian-package-installer file=/tmp/source-config.json hostname=Legion7iPro
2024-07-04T10:38:11.474297Z [info     ] Local file path provided, skipping download [FileDownloader] app_version=1.0.1 application=debian-package-installer file=/tmp/package-config.json hostname=Legion7iPro
2024-07-04T10:38:11.478153Z [info     ] Adding apt sources             [PackageInstaller] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro
2024-07-04T10:38:13.326213Z [info     ] Adding apt source              [SourceAdder] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro source=deb http://aptrepo.effective-range.com stable main
2024-07-04T10:38:13.337605Z [info     ] Key not found, trying to add   [SourceAdder] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main
2024-07-04T10:38:13.340223Z [info     ] Adding key from key server     [SourceAdder] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 key_server=keyserver.ubuntu.com source=deb http://aptrepo.effective-range.com stable main
2024-07-04T10:38:18.664825Z [info     ] Key added                      [SourceAdder] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro key_id=C1AEE2EDBAEC37595801DDFAE15BC62117A4E0F3 source=deb http://aptrepo.effective-range.com stable main
2024-07-04T10:38:18.668500Z [info     ] Updating apt cache             [PackageInstaller] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro
2024-07-04T10:38:30.784501Z [info     ] Installing package             [PackageInstaller] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro package=wifi-manager version=None
2024-07-04T10:38:30.788765Z [info     ] Installing package from repository [AptInstaller] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro package=wifi-manager version=1.0.5
2024-07-04T10:39:25.963260Z [info     ] Package installed successfully [AptInstaller] app_version=1.0.1 application=debian-package-installer hostname=Legion7iPro package=wifi-manager version=1.0.5
...
2024-07-04T10:39:36.638753Z [info     ] [12:39:36] End /tmp/pi-gen/stage2/04-install-packages/01-run.sh [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro
...
2024-07-04T10:41:06.297632Z [info     ] [12:41:06] End /tmp/pi-gen     [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro
2024-07-04T10:41:06.298238Z [info     ] Command execution completed    [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator command=./build.sh elapsed_time=493.999s hostname=Legion7iPro return_code=0
2024-07-04T10:41:06.298498Z [info     ] Image build completed          [ImageBuilder] app_version=0.1.0 application=raspbian-image-generator command=./build.sh hostname=Legion7iPro path=/tmp/pi-gen
2024-07-04T10:41:06.298731Z [info     ] Image found                    [ImageGenerator] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro image=/tmp/pi-gen/deploy/image_2024-07-04-edge-pi-zero-lite.img.xz
2024-07-04T10:41:06.298889Z [info     ] Moving image                   [ImageGenerator] app_version=0.1.0 application=raspbian-image-generator hostname=Legion7iPro source=/tmp/pi-gen/deploy/image_2024-07-04-edge-pi-zero-lite.img.xz target=/home/attilagombos/EffectiveRange/raspbian-image-generator/images/edge-pi-zero-0.2.1.img.xz
```
