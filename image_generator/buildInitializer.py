# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

from context_logger import get_logger
from git import Repo
from package_downloader import PackageConfig
from package_installer import IAptInstaller

from image_generator import TargetConfig, IBuildConfigurator, BuildConfiguration

log = get_logger('BuildInitializer')


class IBuildInitializer(object):

    def initialize(self, config: TargetConfig) -> None:
        raise NotImplementedError()

    def get_repository_path(self) -> str:
        raise NotImplementedError()

    def get_configuration(self) -> BuildConfiguration:
        raise NotImplementedError()


class BuildInitializer(IBuildInitializer):

    def __init__(self, repository: Repo, apt_installer: IAptInstaller, configurator: IBuildConfigurator) -> None:
        self._repository = repository
        self._apt_installer = apt_installer
        self._configurator = configurator

    def initialize(self, config: TargetConfig) -> None:
        self._checkout_target_ref(config)

        self._install_build_dependencies()

        self._configurator.configure(config)

    def get_repository_path(self) -> str:
        return str(self._repository.working_tree_dir) if self._repository else ''

    def get_configuration(self) -> BuildConfiguration:
        return self._configurator.get_configuration()

    def _checkout_target_ref(self, config: TargetConfig) -> None:
        if config.reference not in self._repository.git.show_ref():
            log.error('Reference not exists in repository', reference=config.reference)
            raise AttributeError('Invalid reference')

        log.info('Checking out reference', reference=config.reference)
        self._repository.git.checkout(config.reference)

    def _install_build_dependencies(self) -> None:
        dependency_list = f'{self._repository.working_tree_dir}/depends'

        with open(dependency_list, 'r') as file:
            dependencies = file.readlines()
            dependencies.append('binfmt-support')

            for dependency in dependencies:
                if ':' in dependency:
                    dependency = dependency.split(':')[1]

                config = PackageConfig(package=dependency.strip())

                log.info('Installing build dependency', dependency=config.package)

                if self._apt_installer.install(config):
                    log.info('Dependency installed', dependency=config.package)
                else:
                    log.error('Failed to install dependency', dependency=config.package)
                    raise RuntimeError('Dependency not installed')
