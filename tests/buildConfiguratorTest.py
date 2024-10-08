import os
import unittest
from unittest import TestCase

from common_utility import delete_directory
from context_logger import setup_logging
from package_downloader import PackageConfig, ReleaseConfig
from package_installer import SourceConfig
from test_utility import compare_files

from image_generator import BuildConfigurator, TargetConfig, BuildConfiguration
from tests import TEST_RESOURCE_ROOT, TEST_FILE_SYSTEM_ROOT, create_pi_gen_tree


class BuildConfiguratorTest(TestCase):
    PI_GEN_LOCATION = f'{TEST_FILE_SYSTEM_ROOT}/tmp/pi-gen'

    @classmethod
    def setUpClass(cls) -> None:
        setup_logging('raspbian-image-generator', 'DEBUG', warn_on_overwrite=False)

    def setUp(self) -> None:
        print()
        delete_directory(f'{TEST_RESOURCE_ROOT}/build')
        create_pi_gen_tree(self.PI_GEN_LOCATION)

    def test_build_configuration_generated(self) -> None:
        # Given
        configuration = BuildConfiguration('xz', True, True, '../template/config.j2')
        build_configurator = BuildConfigurator(TEST_RESOURCE_ROOT, self.PI_GEN_LOCATION, configuration)
        config = create_target_config()

        # When
        build_configurator.configure(config)

        # Then
        generated_stage_path = f'{self.PI_GEN_LOCATION}/stage2/02-install-packages'
        self.assertTrue(os.path.exists(f'{generated_stage_path}/files/source-config.json'))
        self.assertTrue(os.path.exists(f'{generated_stage_path}/files/package-config.json'))
        self.assertTrue(os.path.exists(f'{generated_stage_path}/00-packages'))
        self.assertTrue(os.path.exists(f'{generated_stage_path}/01-run.sh'))
        self.assertTrue(os.path.exists(f'{self.PI_GEN_LOCATION}/config'))

        self.assertTrue(
            compare_files(
                f'{TEST_RESOURCE_ROOT}/expected/source-config.json', f'{generated_stage_path}/files/source-config.json'
            )
        )
        self.assertTrue(
            compare_files(
                f'{TEST_RESOURCE_ROOT}/expected/package-config.json',
                f'{generated_stage_path}/files/package-config.json',
            )
        )
        self.assertTrue(compare_files(f'{TEST_RESOURCE_ROOT}/expected/config', f'{self.PI_GEN_LOCATION}/config'))

    def test_build_configuration_generated_with_custom_boot_options(self) -> None:
        # Given
        configuration = BuildConfiguration('xz', True, True, '../template/config.j2')
        build_configurator = BuildConfigurator(TEST_RESOURCE_ROOT, self.PI_GEN_LOCATION, configuration)
        config = create_target_config()
        config.boot_cmdline = ['option1', 'option2']
        config.boot_config = ['option3', 'option4']

        # When
        build_configurator.configure(config)

        # Then
        self.assertEqual(configuration, build_configurator.get_configuration())
        self.assertTrue(
            compare_files(
                f'{TEST_RESOURCE_ROOT}/expected/cmdline.txt',
                f'{self.PI_GEN_LOCATION}/stage1/00-boot-files/files/cmdline.txt',
            )
        )
        self.assertTrue(
            compare_files(
                f'{TEST_RESOURCE_ROOT}/expected/config.txt',
                f'{self.PI_GEN_LOCATION}/stage1/00-boot-files/files/config.txt',
            )
        )
        self.assertTrue(
            compare_files(
                f'{TEST_RESOURCE_ROOT}/expected/07-resize-init.diff',
                f'{self.PI_GEN_LOCATION}/stage2/01-sys-tweaks/00-patches/07-resize-init.diff',
            )
        )

    def test_build_configuration_generated_with_custom_commands(self) -> None:
        # Given
        configuration = BuildConfiguration('xz', True, True, '../template/config.j2')
        build_configurator = BuildConfigurator(TEST_RESOURCE_ROOT, self.PI_GEN_LOCATION, configuration)
        config = create_target_config()
        config.pre_install = ['cmd1', 'cmd2']
        config.post_install = ['cmd3', 'cmd4']

        # When
        build_configurator.configure(config)

        # Then
        generated_stage_path = f'{self.PI_GEN_LOCATION}/stage2/02-install-packages'
        self.assertTrue(os.path.exists(f'{generated_stage_path}/00-packages'))
        self.assertTrue(os.path.exists(f'{generated_stage_path}/01-run-chroot.sh'))
        self.assertTrue(os.path.exists(f'{generated_stage_path}/02-run.sh'))
        self.assertTrue(os.path.exists(f'{generated_stage_path}/03-run-chroot.sh'))

        self.assertTrue(
            compare_files(f'{TEST_RESOURCE_ROOT}/expected/pre-install.sh', f'{generated_stage_path}/01-run-chroot.sh')
        )
        self.assertTrue(
            compare_files(f'{TEST_RESOURCE_ROOT}/expected/post-install.sh', f'{generated_stage_path}/03-run-chroot.sh')
        )

    def test_build_configuration_generated_first_boot_commands(self) -> None:
        # Given
        configuration = BuildConfiguration('xz', True, True, '../template/config.j2', '../template/first_boot.j2')
        build_configurator = BuildConfigurator(TEST_RESOURCE_ROOT, self.PI_GEN_LOCATION, configuration)
        config = create_target_config()
        config.first_boot = ['cmd1', 'cmd2']

        # When
        build_configurator.configure(config)

        # Then
        generated_stage_path = f'{self.PI_GEN_LOCATION}/stage2/02-install-packages'
        self.assertTrue(os.path.exists(f'{generated_stage_path}/00-packages'))
        self.assertTrue(os.path.exists(f'{generated_stage_path}/01-run.sh'))

        self.assertTrue(
            compare_files(
                f'{TEST_RESOURCE_ROOT}/expected/first-boot.sh',
                f'{self.PI_GEN_LOCATION}/stage2/01-sys-tweaks/files/rc.local',
            )
        )


def create_target_config() -> TargetConfig:
    return TargetConfig(
        name='test-target',
        version='1.0.0',
        reference='test-ref',
        sources=[
            SourceConfig(
                name='source1',
                source='deb http://url1 stable main',
                key_id='0123456789ABCDEF012345671111111111111111',
                key_file='http://url1/dists/stable/public1.key',
                key_server='keyserver.test1.com',
            ),
            SourceConfig(
                name='source2',
                source='deb http://url2 stable main',
                key_id='0123456789ABCDEF012345672222222222222222',
                key_file='http://url2/dists/stable/public2.key',
            ),
            SourceConfig(
                name='source3',
                source='deb http://url3 stable main',
                key_id='0123456789ABCDEF012345673333333333333333',
                key_file='/path/to/public3.key',
            ),
        ],
        packages=[
            PackageConfig(
                package='package1',
                version='1.0.0',
                release=ReleaseConfig(owner='owner1', repo='repo1', tag='v1.0.0', token='token1', matcher='*.deb'),
            ),
            PackageConfig(package='package2', version='2.0.0', file_url='url2'),
            PackageConfig(
                package='package3',
                release=ReleaseConfig(owner='owner3', repo='repo3', tag='v3.0.0', token='$TEST_TOKEN', matcher='*.deb'),
            ),
            PackageConfig(
                package='package4',
                file_url='url4',
                release=ReleaseConfig(owner='owner4', repo='repo4', tag='v4.0.0', matcher='*.deb'),
            ),
        ],
    )


if __name__ == '__main__':
    unittest.main()
