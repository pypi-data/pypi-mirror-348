from setuptools import setup, find_packages
MAJOR =0
MINOR =2
PATCH =0
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

def get_install_requires():
    reqs = [
    'aiohappyeyeballs',
    'aiohttp',
    'aioredis',
    'aiosignal',
    'annotated-types',
    'async-timeout',
    'attrs',
    'backports.tarfile',
    'certifi',
    'charset-normalizer',
    'colorama',
    'docutils',
    'frozenlist',
    'id',
    'idna',
    'importlib_metadata',
    'jaraco.classes',
    'jaraco.context',
    'jaraco.functools',
    'keyring',
    'loguru',
    'markdown-it-py',
    'mdurl',
    'more-itertools',
    'multidict',
    'nh3',
    'packaging',
    'propcache',
    'pydantic',
    'pydantic_core',
    'Pygments',
    'pywin32-ctypes',
    'readme_renderer',
    'redis',
    'requests',
    'requests-toolbelt',
    'rfc3986',
    'rich',
    'typing-inspection',
    'typing_extensions',
    'urllib3',
    'win32_setctime',
    'yarl',
    'zipp',
    'nacos-sdk-python',
    'uvicorn',
    'fastapi',
    'sqlalchemy'
]
    return reqs


setup(
    name='fastdevcommon',
    version=VERSION,
    packages=find_packages(),
    description='A common development component',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hwzlikewyh/FastDevCommon.git',
    author='hwzlikewyh',
    author_email='hwzlikewyh@163.com',
    license='MIT',
    install_requires=get_install_requires(),
    package_data={'': ['*.csv', '*.txt', '.toml']},  # 这个很重要
    include_package_data=True  # 也选上
)
