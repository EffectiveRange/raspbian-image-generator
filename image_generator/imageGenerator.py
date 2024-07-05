# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
import shutil
from datetime import datetime

from context_logger import get_logger
from package_downloader import IJsonLoader

from image_generator import TargetConfig, IImageBuilder, IBuildInitializer

log = get_logger('ImageGenerator')


class ImageGenerator(object):

    def __init__(self, config_path: str, json_loader: IJsonLoader, initializer: IBuildInitializer,
                 image_builder: IImageBuilder, output_dir: str,
                 output_pattern: str = '{target}-{version}') -> None:
        self._config_path = config_path
        self._json_loader = json_loader
        self._initializer = initializer
        self._image_builder = image_builder
        self._output_dir = output_dir
        self._output_pattern = output_pattern

    def generate(self, target_name: str) -> TargetConfig:
        config = self._get_config(target_name)

        self._initializer.initialize(config)

        self._image_builder.build()

        image_path = self._get_image_path(config)

        self._check_result(image_path)

        self._move_image(image_path, config)

        return config

    def _get_config(self, target_name: str) -> TargetConfig:
        log.info('Loading target configuration', target=target_name)

        config_list = self._json_loader.load_list(self._config_path, TargetConfig)
        config_map = {config.name: config for config in config_list}

        if not (target := config_map.get(target_name)):
            log.error('Target configuration not found', target=target_name, target_list=list(config_map.keys()))
            raise AttributeError('Invalid target name or configuration list')

        return target

    def _get_image_path(self, config: TargetConfig) -> str:
        date = datetime.now().strftime('%Y-%m-%d')
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

    def _move_image(self, image_path: str, config: TargetConfig) -> None:
        file_type = self._get_file_type()
        image_name = self._output_pattern.format(target=config.name, version=config.version)
        output_path = f'{self._output_dir}/{config.name}/{config.version}'
        target_image_path = f'{output_path}/{image_name}.{file_type}'

        log.info('Moving image', source=image_path, target=target_image_path)

        os.makedirs(output_path, exist_ok=True)

        if os.path.exists(target_image_path):
            os.unlink(target_image_path)

        shutil.move(image_path, target_image_path)

    def _get_file_type(self) -> str:
        compression_to_file_type = {
            'none': 'img',
            'zip': 'zip',
            'gz': 'img.gz',
            'xz': 'img.xz'
        }

        compression = self._initializer.get_configuration().compression

        return compression_to_file_type.get(compression, 'img')
