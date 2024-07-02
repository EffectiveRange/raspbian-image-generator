#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
import shutil
from argparse import Namespace, ArgumentParser, ArgumentDefaultsHelpFormatter, BooleanOptionalAction
from pathlib import Path

from apt import Cache
from context_logger import setup_logging, get_logger
from git import Repo
from package_downloader import JsonLoader, FileDownloader, SessionProvider
from package_installer import AptInstaller

from image_generator import ImageGenerator, BuildConfigurator, ImageBuilder, BuildConfiguration, \
    BuildInitializer

log = get_logger('ImageGeneratorApp')


def main() -> None:
    arguments = _get_arguments()

    setup_logging('raspbian-image-generator', arguments.log_level, arguments.log_file)

    log.info('Started image generation', target=arguments.target_name, arguments=vars(arguments))

    resource_root = _get_resource_root()
    repository_location = os.path.abspath(arguments.repository_path)
    repository = _initialize_repository(repository_location, arguments.repository_url)

    session_provider = SessionProvider()
    file_downloader = FileDownloader(session_provider, os.path.abspath(arguments.download))

    target_config = file_downloader.download(arguments.target_config, skip_if_exists=False)
    json_loader = JsonLoader()

    apt_cache = Cache()
    apt_installer = AptInstaller(apt_cache)

    configuration = BuildConfiguration(arguments.compression, arguments.enable_ssh, arguments.clean_build,
                                       arguments.config_template)
    configurator = BuildConfigurator(resource_root, repository_location, configuration)
    image_builder = ImageBuilder(repository_location)

    build_initializer = BuildInitializer(repository, apt_installer, configurator)
    output_directory = os.path.abspath(arguments.output)
    image_generator = ImageGenerator(target_config, json_loader, build_initializer, image_builder, output_directory)

    image_generator.generate(arguments.target_name)


def _get_arguments() -> Namespace:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--log-file', help='log file path')
    parser.add_argument('-l', '--log-level', help='logging level', default='INFO')

    parser.add_argument('-d', '--download', help='target config download location', default='/tmp/config')
    parser.add_argument('-p', '--repository-path', help='repository location path', default='/tmp/pi-gen')
    parser.add_argument('-u', '--repository-url', help='repository URL',
                        default='https://github.com/RPi-Distro/pi-gen.git')
    parser.add_argument('-o', '--output', help='output image directory', default='images')

    parser.add_argument('-t', '--config-template', help='pi-gen config template', default='config/config.template')
    parser.add_argument('-c', '--compression', help='output image compression', default='xz')
    parser.add_argument('--enable-ssh', help='enable SSH access', action=BooleanOptionalAction, default=True)
    parser.add_argument('--clean-build', help='clean before build', action=BooleanOptionalAction, default=True)

    parser.add_argument('target_config', help='target config JSON file or URL')
    parser.add_argument('target_name', help='image target config name')

    return parser.parse_args()


def _get_resource_root() -> str:
    return str(Path(os.path.dirname(__file__)).parent.absolute())


def _initialize_repository(repo_path: str, repo_url: str) -> Repo:
    if not os.path.exists(f'{repo_path}/.git'):
        shutil.rmtree(repo_path, ignore_errors=True)
        log.info('Cloning repository', repository=repo_url, path=repo_path)
        return Repo.clone_from(repo_url, repo_path)
    else:
        log.info('Cleaning existing repository', repository=repo_url, path=repo_path)
        repo = Repo(repo_path)
        repo.git.reset('--hard', 'HEAD')
        repo.git.clean('-df')
        return repo


if __name__ == '__main__':
    main()
