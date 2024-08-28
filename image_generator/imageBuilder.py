# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os
import re
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from logging import DEBUG, WARNING
from subprocess import PIPE, Popen, CalledProcessError
from typing import Optional

from context_logger import get_logger

log = get_logger('ImageBuilder')


class IImageBuilder(object):

    def build(self, command: str = './build.sh') -> datetime:
        raise NotImplementedError()


class ImageBuilder(IImageBuilder):

    def __init__(self, repository_path: str) -> None:
        self._repository_path = repository_path
        self._stage_stack: list[str] = []

    def build(self, command: str = './build.sh') -> datetime:
        start_time = datetime.now()

        log.info('Building image', path=self._repository_path, command=command, start_time=start_time)

        os.chdir(self._repository_path)

        return_code = self._run_command(command)

        if return_code:
            log.error(
                'Failed to build image',
                path=self._repository_path,
                return_code=return_code,
                command=command,
                stage=self._get_current_stage(),
            )
            raise CalledProcessError(return_code, command)

        log.info('Image build completed', path=self._repository_path, command=command)

        return start_time

    def _run_command(self, command: str) -> Optional[int]:
        log.info('Executing command', command=command)

        start_time = time.time()

        with Popen(command, shell=True, text=True, stdout=PIPE, stderr=PIPE) as process:
            with ThreadPoolExecutor(2) as pool:
                exhaust = partial(pool.submit, partial(deque, maxlen=0))
                if process.stdout:
                    exhaust(self._log_output(line[:-1], DEBUG) for line in process.stdout)
                if process.stderr:
                    exhaust(self._log_output(line[:-1], WARNING) for line in process.stderr)

        end_time = time.time()
        elapsed_time = end_time - start_time

        log.info(
            'Command execution completed',
            command=command,
            return_code=process.returncode,
            elapsed_time=f'{elapsed_time:.3f}s',
        )

        return process.poll()

    def _log_output(self, log_line: str, log_level: int) -> str:
        if self._is_package_installer_log(log_line):
            print(log_line)
        elif self._is_pi_gen_log(log_line):
            log.info(log_line)
            self._handle_stage_stack(log_line)
        else:
            log.log(log_level, log_line, stage=self._get_current_stage())
        return log_line

    def _is_package_installer_log(self, log_line: str) -> bool:
        return 'package-installer\x1b' in log_line

    def _is_pi_gen_log(self, log_line: str) -> bool:
        return log_line.startswith('[') and '/pi-gen' in log_line

    def _handle_stage_stack(self, log_line: str) -> None:
        match_begin = re.match(r'^\[.*] Begin (.*)', log_line)
        if match_begin:
            stage = match_begin.group(1).replace(f'{self._repository_path}', '')[1:]
            self._stage_stack.append(stage)
        elif re.match(r'^\[.*] End (.*)', log_line):
            self._stage_stack.pop()

    def _get_current_stage(self) -> Optional[str]:
        return self._stage_stack[-1] if self._stage_stack else None
