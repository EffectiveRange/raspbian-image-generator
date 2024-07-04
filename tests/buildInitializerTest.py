import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from context_logger import setup_logging
from git import Repo
from package_installer import IAptInstaller

from image_generator import IBuildConfigurator, TargetConfig, BuildConfiguration, BuildInitializer
from tests.utils import TEST_RESOURCE_ROOT, TEST_FILE_SYSTEM_ROOT, delete_directory, create_pi_gen_tree


class BuildInitializerTest(TestCase):
    PI_GEN_LOCATION = f'{TEST_FILE_SYSTEM_ROOT}/tmp/pi-gen'

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging('raspbian-image-generator', 'DEBUG', warn_on_overwrite=False)

    def setUp(self) -> None:
        print()
        delete_directory(f'{TEST_RESOURCE_ROOT}/deploy')
        create_pi_gen_tree(self.PI_GEN_LOCATION)

    def test_returns_repository_working_tree(self) -> None:
        # Given
        repository, apt_installer, configurator = create_mocks()
        build_initializer = BuildInitializer(repository, apt_installer, configurator)

        # When
        result = build_initializer.get_repository_path()

        # Then
        self.assertEqual(result, repository.working_tree_dir)

    def test_returns_build_configuration(self) -> None:
        # Given
        repository, apt_installer, configurator = create_mocks()
        build_initializer = BuildInitializer(repository, apt_installer, configurator)

        # When
        result = build_initializer.get_configuration()

        # Then
        self.assertEqual(result, configurator.get_configuration())

    def test_build_successfully_initialized(self) -> None:
        # Given
        config = TargetConfig(name='test-target', version='1.0.0', reference='test-ref', sources=[], packages=[])
        repository, apt_installer, configurator = create_mocks()
        build_initializer = BuildInitializer(repository, apt_installer, configurator)

        # When
        build_initializer.initialize(config)

        # Then
        repository.git.checkout.assert_called_once_with('test-ref')
        apt_installer.install.assert_called()
        configurator.configure.assert_called_once_with(config)

    def test_raises_error_when_target_reference_not_found(self) -> None:
        # Given
        config = TargetConfig(name='test-target', version='1.0.0', reference='invalid-ref', sources=[], packages=[])
        repository, apt_installer, configurator = create_mocks()
        build_initializer = BuildInitializer(repository, apt_installer, configurator)

        # When
        self.assertRaises(AttributeError, build_initializer.initialize, config)

        # Then
        repository.git.checkout.assert_not_called()
        apt_installer.install.assert_not_called()
        configurator.configure.assert_not_called()

    def test_raises_error_when_failed_to_install_build_dependency(self) -> None:
        # Given
        config = TargetConfig(name='test-target', version='1.0.0', reference='test-ref', sources=[], packages=[])
        repository, apt_installer, configurator = create_mocks()
        apt_installer.install.side_effect = [True, False]
        build_initializer = BuildInitializer(repository, apt_installer, configurator)

        # When
        self.assertRaises(RuntimeError, build_initializer.initialize, config)

        # Then
        repository.git.checkout.assert_called_once_with('test-ref')
        configurator.configure.assert_not_called()


def create_mocks() -> tuple:
    repository = MagicMock(spec=Repo)
    repository.git.show_ref.return_value = 'test-ref'
    repository.working_tree_dir = f'{TEST_FILE_SYSTEM_ROOT}/tmp/pi-gen'
    apt_installer = MagicMock(spec=IAptInstaller)
    configurator = MagicMock(spec=IBuildConfigurator)
    configurator.get_configuration.return_value = BuildConfiguration('xz', True, True, 'config/config.template')
    return repository, apt_installer, configurator


if __name__ == '__main__':
    unittest.main()
