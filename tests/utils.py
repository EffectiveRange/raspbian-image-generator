import os
from pathlib import Path

from common_utility import delete_directory, copy_file

TEST_RESOURCE_ROOT = str(Path(os.path.dirname(__file__)).absolute())
TEST_FILE_SYSTEM_ROOT = str(Path(TEST_RESOURCE_ROOT).joinpath('test_root').absolute())
RESOURCE_ROOT = str(Path(TEST_RESOURCE_ROOT).parent.absolute())


def create_pi_gen_tree(pi_gen_path: str) -> None:
    delete_directory(TEST_FILE_SYSTEM_ROOT)
    os.makedirs(pi_gen_path, exist_ok=True)
    deploy_dir = f'{pi_gen_path}/deploy'
    os.makedirs(deploy_dir, exist_ok=True)
    copy_file(f'{TEST_RESOURCE_ROOT}/config/before-install.list', deploy_dir)
    copy_file(f'{TEST_RESOURCE_ROOT}/config/after-install.list', deploy_dir)
    boot_files_path = f'{pi_gen_path}/stage1/00-boot-files/files'
    os.makedirs(boot_files_path, exist_ok=True)
    copy_file(f'{TEST_RESOURCE_ROOT}/config/cmdline.txt', boot_files_path)
    copy_file(f'{TEST_RESOURCE_ROOT}/config/config.txt', boot_files_path)
    stage_2_path = f'{pi_gen_path}/stage2'
    os.makedirs(stage_2_path, exist_ok=True)
    stage_2_sub_stage_00_path = f'{stage_2_path}/00-copies-and-fills'
    os.makedirs(stage_2_sub_stage_00_path, exist_ok=True)
    stage_2_sub_stage_01_path = f'{stage_2_path}/01-sys-tweaks'
    os.makedirs(stage_2_sub_stage_01_path, exist_ok=True)
    copy_file(
        f'{TEST_RESOURCE_ROOT}/config/07-resize-init.diff',
        f'{pi_gen_path}/stage2/01-sys-tweaks/00-patches/07-resize-init.diff',
    )
    copy_file(
        f'{TEST_RESOURCE_ROOT}/config/rc.local',
        f'{pi_gen_path}/stage2/01-sys-tweaks/files/rc.local',
    )
    copy_file(f'{TEST_RESOURCE_ROOT}/config/depends', pi_gen_path)
