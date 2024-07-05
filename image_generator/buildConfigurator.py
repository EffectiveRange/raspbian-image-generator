# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
import re
import shutil

from context_logger import get_logger
from package_downloader import T
from pydantic import TypeAdapter

from image_generator import TargetConfig, render_template_file, write_file

log = get_logger('BuildConfigurator')


class BuildConfiguration(object):

    def __init__(self, compression: str, enable_ssh: bool, clean_build: bool, template: str) -> None:
        self.compression = compression
        self.enable_ssh = '1' if enable_ssh else '0'
        self.clean_build = '1' if clean_build else '0'
        self.template = template


class IBuildConfigurator(object):

    def get_configuration(self) -> BuildConfiguration:
        raise NotImplementedError()

    def configure(self, config: TargetConfig) -> None:
        raise NotImplementedError()


class BuildConfigurator(IBuildConfigurator):

    def __init__(self, resource_root: str, repository_location: str, configuration: BuildConfiguration,
                 sub_stage_name: str = 'install-packages') -> None:
        self._resource_root = resource_root
        self._repository_location = repository_location
        self._configuration = configuration
        self._sub_stage_name = sub_stage_name
        self._temp_sub_stage = f'{self._resource_root}/build/{self._sub_stage_name}'

    def get_configuration(self) -> BuildConfiguration:
        return self._configuration

    def configure(self, config: TargetConfig) -> None:
        log.info('Configuring build')

        self._update_boot_files(config)

        self._build_sub_stage(config)

        self._append_stage(config.stage)

        self._create_build_config(config)

    def _update_boot_files(self, config: TargetConfig) -> None:
        if config.boot_cmdline:
            cmdline_path = f'{self._repository_location}/stage1/00-boot-files/files/cmdline.txt'

            log.info('Appending boot command line options', file=cmdline_path, options=config.boot_cmdline)

            with open(cmdline_path, 'r') as cmdline_file:
                cmdline = cmdline_file.read().rstrip('\n')

            with open(cmdline_path, 'w') as cmdline_file:
                cmdline_options = ' '.join(config.boot_cmdline)
                new_cmdline = f'{cmdline} {cmdline_options}'
                cmdline_file.write(f'{new_cmdline}\n')

            patch_path = f'{self._repository_location}/stage2/01-sys-tweaks/00-patches/07-resize-init.diff'

            with open(patch_path, 'r') as patch_file:
                patch = patch_file.read()

            with open(patch_path, 'w') as patch_file:
                patch_file.write(patch.replace(cmdline, new_cmdline))

        if config.boot_config:
            config_path = f'{self._repository_location}/stage1/00-boot-files/files/config.txt'

            log.info('Appending boot config options', file=config_path, options=config.boot_config)

            with open(config_path, 'a') as config_file:
                config_options = '\n'.join(config.boot_config)
                config_file.write(f'{config_options}\n')

    def _build_sub_stage(self, config: TargetConfig) -> None:
        log.info('Creating sub-stage', stage=f'stage{config.stage}', sub_stage=self._temp_sub_stage)

        os.makedirs(self._temp_sub_stage, exist_ok=True)

        self._create_config_files(config)

        self._copy_sub_stage_scripts()

    def _append_stage(self, stage: int) -> None:
        new_sub_stage_dir = self._create_sub_stage_dir(stage)

        log.info('Appending sub-stage to stage', stage=f'stage{stage}', sub_stage=new_sub_stage_dir)

        self._copy_build_files(new_sub_stage_dir)

    def _create_build_config(self, config: TargetConfig) -> None:
        context = {
            'target_name': config.name,
            'target_hostname': config.name,
            'compression': self._configuration.compression,
            'enable_ssh': self._configuration.enable_ssh,
            'clean_build': self._configuration.clean_build,
            'stage_list': ' '.join([f'stage{i}' for i in range(config.stage + 1)])
        }

        build_config = render_template_file(self._resource_root, self._configuration.template, context)

        config_path = f'{self._repository_location}/config'
        log.info('Creating build config file', file=config_path)
        write_file(config_path, build_config)

    def _create_sub_stage_dir(self, target_stage: int) -> str:
        stage_dir = f'{self._repository_location}/stage{target_stage}'

        new_index = self._get_new_sub_dir_index(stage_dir)
        new_sub_stage_name = f'{str(new_index).zfill(2)}-{self._sub_stage_name}'

        new_sub_stage_dir = f'{stage_dir}/{new_sub_stage_name}'
        os.makedirs(new_sub_stage_dir, exist_ok=True)

        return new_sub_stage_dir

    def _get_new_sub_dir_index(self, stage_dir: str) -> int:
        indexes = []

        sub_dirs = [sub_dir for sub_dir in os.listdir(stage_dir) if os.path.isdir(f'{stage_dir}/{sub_dir}')]

        for sub_dir in sub_dirs:
            starts_with_digits = re.match(r'^\d+', sub_dir)
            if starts_with_digits:
                indexes.append(int(starts_with_digits.group()))

        return max(indexes) + 1 if indexes else 0

    def _create_config_files(self, config: TargetConfig) -> None:
        files_dir = f'{self._temp_sub_stage}/files'
        os.makedirs(files_dir, exist_ok=True)

        if config.sources:
            source_config_path = f'{files_dir}/source-config.json'

            log.info('Creating source config file', file=source_config_path)

            self._create_config_file(source_config_path, config.sources)

        package_config_path = f'{files_dir}/package-config.json'

        log.info('Creating package config file', file=package_config_path)

        self._create_config_file(package_config_path, config.packages)

    def _copy_sub_stage_scripts(self) -> None:
        scripts_path = f'{self._resource_root}/scripts'
        os.system(f'chmod -R +x {scripts_path}')
        scripts = os.listdir(scripts_path)
        scripts.sort()
        log.info('Copying sub-stage scripts', scripts=scripts)
        shutil.copytree(scripts_path, self._temp_sub_stage, dirs_exist_ok=True)

    def _copy_build_files(self, new_sub_stage_dir: str) -> None:
        shutil.copytree(self._temp_sub_stage, new_sub_stage_dir, dirs_exist_ok=True)

    def _create_config_file(self, config_path: str, config_list: list[T]) -> None:
        with open(config_path, 'w') as config_file:
            type_adapter = TypeAdapter(config_list.__class__)
            config_file.write(f'{type_adapter.dump_json(config_list, indent=2, exclude_none=True).decode()}\n')
