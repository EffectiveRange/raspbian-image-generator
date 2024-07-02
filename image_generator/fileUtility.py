# SPDX-FileCopyrightText: 2024 Ferenc Nandor Janky <ferenj@effective-range.com>
# SPDX-FileCopyrightText: 2024 Attila Gombos <attila.gombos@effective-range.com>
# SPDX-License-Identifier: MIT

import os

from jinja2 import Environment, FileSystemLoader


def write_file(file_path: str, content: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)


def render_template_file(resource_root: str, template_file: str, context: dict[str, str]) -> str:
    template_path = f'{resource_root}/{template_file}'
    environment = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = environment.get_template(os.path.basename(template_path))
    return f'{template.render(context)}\n'
