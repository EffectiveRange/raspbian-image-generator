from setuptools import setup

setup(
    name='raspbian-image-generator',
    version='1.3.1',
    description='Raspberry Pi image generator using the official pi-gen repository',
    author='Ferenc Nandor Janky & Attila Gombos',
    author_email='info@effective-range.com',
    packages=['image_generator'],
    scripts=['bin/raspbian-image-generator.py'],
    data_files=[
        ('template', ['template/config.j2', 'template/first_boot.j2']),
        ('scripts', ['scripts/packages', 'scripts/run.sh']),
    ],
    install_requires=[
        'GitPython',
        'jinja2',
        'pydantic',
        'python-context-logger@git+https://github.com/EffectiveRange/python-context-logger.git@latest',
        'debian-package-installer' '@git+https://github.com/EffectiveRange/debian-package-installer.git@latest',
    ],
)
