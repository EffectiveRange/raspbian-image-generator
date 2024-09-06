import unittest
from subprocess import CalledProcessError
from unittest import TestCase

from common_utility import copy_file
from context_logger import setup_logging

from image_generator import ImageBuilder
from tests import TEST_RESOURCE_ROOT, TEST_FILE_SYSTEM_ROOT


class ImageBuilderTest(TestCase):
    PI_GEN_LOCATION = f'{TEST_FILE_SYSTEM_ROOT}/tmp/pi-gen'

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging('raspbian-image-generator', 'DEBUG', warn_on_overwrite=False)

    def setUp(self) -> None:
        print()
        copy_file(f'{TEST_RESOURCE_ROOT}/scripts/build.sh', self.PI_GEN_LOCATION)

    def test_successful_build(self):
        # Given
        image_builder = ImageBuilder(self.PI_GEN_LOCATION)

        # When
        image_builder.build(f'/bin/bash ./build.sh 0 {self.PI_GEN_LOCATION}')

        # Then
        # No exception should be thrown

    def test_failing_build(self):
        # Given
        image_builder = ImageBuilder(self.PI_GEN_LOCATION)

        # When, Then
        self.assertRaises(CalledProcessError, image_builder.build, f'/bin/bash ./build.sh 1 {self.PI_GEN_LOCATION}')


if __name__ == '__main__':
    unittest.main()
