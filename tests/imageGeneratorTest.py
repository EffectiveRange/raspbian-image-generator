import os
import subprocess
import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from context_logger import setup_logging
from package_downloader import IJsonLoader

from image_generator import ImageGenerator, IImageBuilder, TargetConfig, BuildConfiguration, IBuildInitializer
from tests.utils import TEST_RESOURCE_ROOT, TEST_FILE_SYSTEM_ROOT, delete_directory, create_pi_gen_tree


class ImageGeneratorTest(TestCase):
    PI_GEN_LOCATION = f'{TEST_FILE_SYSTEM_ROOT}/tmp/pi-gen'
    OUTPUT_DIR = f'{TEST_RESOURCE_ROOT}/images'

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging('raspbian-image-generator', 'DEBUG', warn_on_overwrite=False)

    def setUp(self) -> None:
        print()
        delete_directory(f'{TEST_RESOURCE_ROOT}/deploy')
        delete_directory(f'{TEST_RESOURCE_ROOT}/images')
        create_pi_gen_tree(self.PI_GEN_LOCATION)

    def test_image_successfully_generated(self) -> None:
        # Given
        config = TargetConfig(name='test-target', version='1.0.0', reference='test-ref', sources=[], packages=[])
        json_loader, initializer, builder = create_mocks(config)
        image_generator = ImageGenerator('/path/to/config', json_loader, initializer, builder, self.OUTPUT_DIR)
        subprocess.run(['/bin/bash', f'{TEST_RESOURCE_ROOT}/scripts/build.sh', '0', f'{self.PI_GEN_LOCATION}'])

        # When
        image_generator.generate('test-target')

        # Then
        json_loader.load_list.assert_called_once()
        initializer.initialize.assert_called_once_with(config)
        builder.build.assert_called_once()
        self.assertTrue(os.path.exists(f'{TEST_RESOURCE_ROOT}/images/test-target_1.0.0.img.xz'))

    def test_raises_error_when_target_not_found(self) -> None:
        # Given
        config = TargetConfig(name='test-target', version='1.0.0', reference='test-ref', sources=[], packages=[])
        json_loader, initializer, builder = create_mocks(config)
        image_generator = ImageGenerator('/path/to/config', json_loader, initializer, builder, self.OUTPUT_DIR)

        # When
        self.assertRaises(AttributeError, image_generator.generate, 'invalid-target')

        # Then
        json_loader.load_list.assert_called_once()
        initializer.initialize.assert_not_called()
        builder.build.assert_not_called()

    def test_raises_error_when_image_not_found(self):
        # Given
        config = TargetConfig(name='test-target', version='1.0.0', reference='test-ref', sources=[], packages=[])
        json_loader, initializer, builder = create_mocks(config)
        image_generator = ImageGenerator('/path/to/config', json_loader, initializer, builder, self.OUTPUT_DIR)

        # When
        self.assertRaises(FileNotFoundError, image_generator.generate, 'test-target')

        # Then
        json_loader.load_list.assert_called_once()
        initializer.initialize.assert_called_once_with(config)
        builder.build.assert_called_once()


def create_mocks(target: TargetConfig) -> tuple:
    json_loader = MagicMock(spec=IJsonLoader)
    json_loader.load_list.return_value = [target]
    initializer = MagicMock(spec=IBuildInitializer)
    initializer.get_repository_path.return_value = f'{TEST_FILE_SYSTEM_ROOT}/tmp/pi-gen'
    initializer.get_configuration.return_value = BuildConfiguration('xz', True, True, 'config/config.template')
    builder = MagicMock(spec=IImageBuilder)
    return json_loader, initializer, builder


if __name__ == '__main__':
    unittest.main()
