from setuptools import find_packages, setup
from typing import List


def parse_requirements(file_name: str) -> List[str]:
    with open(file_name) as f:
        return [
            require.strip() for require in f
            if require.strip() and not require.startswith('#')
        ]


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


version_file = 'qtars/version.py'


def get_version():
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


setup(
    name='q-tars',
    version=get_version(),
    description=
    'Q-TARS: Omini Agent Framework based on Multi-modal Reinforcement Learning',
    author='wangxingjun778',
    author_email='wangxingjun778@163.com',
    keywords='Multi-modal,Agent, RL',
    url='https://github.com/wabc/Q-TARS',
    license='Apache License 2.0',
    packages=find_packages(exclude=['*test*', 'demo']),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt'),
    long_description=readme(),
    long_description_content_type='text/markdown',
    package_data={},
)
