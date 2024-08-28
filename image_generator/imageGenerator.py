# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import difflib
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime

from context_logger import get_logger
from package_downloader import IJsonLoader

from image_generator import TargetConfig, IImageBuilder, IBuildInitializer

log = get_logger('ImageGenerator')


@dataclass
class ImageProperties:
    directory: str
    name: str
    type: str

    @property
    def path(self) -> str:
        return f'{self.directory}/{self.name}.{self.type}'


class ImageGenerator(object):

    def __init__(
        self,
        config_path: str,
        json_loader: IJsonLoader,
        initializer: IBuildInitializer,
        image_builder: IImageBuilder,
        output_dir: str,
        output_pattern: str = '{target}-{version}',
    ) -> None:
        self._config_path = config_path
        self._json_loader = json_loader
        self._initializer = initializer
        self._image_builder = image_builder
        self._output_dir = output_dir
        self._output_pattern = output_pattern

    def generate(self, target_name: str) -> TargetConfig:
        config = self._get_config(target_name)

        self._initializer.initialize(config)

        start_time = self._image_builder.build()

        source_image_path = self._get_source_image_path(config, start_time)

        self._check_result(source_image_path)

        image_properties = self._create_image_properties(config)

        self._move_image(source_image_path, image_properties)

        self._export_config(config, image_properties)

        self._export_package_list(image_properties)

        return config

    def _get_config(self, target_name: str) -> TargetConfig:
        log.info('Loading target configuration', target=target_name)

        config_list = self._json_loader.load_list(self._config_path, TargetConfig)
        config_map = {config.name: config for config in config_list}

        if not (target := config_map.get(target_name)):
            log.error('Target configuration not found', target=target_name, target_list=list(config_map.keys()))
            raise AttributeError('Invalid target name or configuration list')

        log.info('Target configuration loaded', target=target_name, version=target.version)

        return target

    def _get_source_image_path(self, config: TargetConfig, start_time: datetime) -> str:
        date = start_time.strftime('%Y-%m-%d')
        file_type = self._get_file_type()
        image_name_pattern = 'image_{date}-{target}-lite.{type}'

        image_name = image_name_pattern.format(date=date, target=config.name, type=file_type)

        return f'{self._initializer.get_repository_path()}/deploy/{image_name}'

    def _check_result(self, image_path: str) -> None:
        if not os.path.exists(image_path):
            log.error('Image not found', image=image_path)
            raise FileNotFoundError('Image not found')
        else:
            log.info('Image found', image=image_path)

    def _create_image_properties(self, config: TargetConfig) -> ImageProperties:
        return ImageProperties(
            directory=f'{self._output_dir}/{config.name}/{config.version}',
            name=self._output_pattern.format(target=config.name, version=config.version),
            type=self._get_file_type(),
        )

    def _move_image(self, source_image_path: str, image_properties: ImageProperties) -> None:
        log.info('Moving image', source=source_image_path, target=image_properties.path)

        os.makedirs(image_properties.directory, exist_ok=True)

        if os.path.exists(image_properties.path):
            os.unlink(image_properties.path)

        shutil.move(source_image_path, image_properties.path)

    def _export_config(self, config: TargetConfig, image_properties: ImageProperties) -> None:
        export_path = f'{image_properties.directory}/{image_properties.name}.json'
        log.info('Exporting target configuration to file', file=export_path)

        with open(export_path, 'w') as config_file:
            config_file.write(f'{config.model_dump_json(indent=2, exclude_none=True)}\n')

    def _get_file_type(self) -> str:
        compression_to_file_type = {'none': 'img', 'zip': 'zip', 'gz': 'img.gz', 'xz': 'img.xz'}

        compression = self._initializer.get_configuration().compression

        return compression_to_file_type.get(compression, 'img')

    def _export_package_list(self, image_properties: ImageProperties) -> None:
        package_list_dir = f'{self._initializer.get_repository_path()}/deploy'
        before_install = f'{package_list_dir}/before-install.list'
        after_install = f'{package_list_dir}/after-install.list'

        with open(before_install, 'r') as before_file, open(after_install, 'r') as after_file:
            pattern = r'\[.*?\]'
            before = re.sub(pattern, '', before_file.read()).splitlines()
            after = re.sub(pattern, '', after_file.read()).splitlines()
            diff = difflib.ndiff(before, after)

        export_path = f'{image_properties.directory}/{image_properties.name}.list'

        installed_packages = [package.strip('+ ') for package in diff if package.startswith('+')]

        log.info('Exporting installed package list to file', file=export_path)

        with open(export_path, 'w') as installed_file:
            installed_file.write('\n'.join(installed_packages) + '\n')
