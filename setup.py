from setuptools import find_packages
from setuptools import setup

setup(name='zedscraps',
      version='0.1',
      description='_scraps',
      url='',
      author='Vito De Tullio',
      author_email='vito.detullio@gmail.com',
      license='GPL3',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['marshmallow-dataclass[enum,union]',
                        'dataclasses-json',
                        'vosk',
                        'sounddevice',
                        'quart-trio',
                        'trio',
                        'mypy',
                        # 'pyaudio',
                        'trio_typing',
                        'isort'],
      entry_points={'console_scripts': ['mm=mm:main',
                                        'executable=executable:main',
                                        'dtj=dtj:main',
                                        'rubinetto=rubinetto.__main__:main'],
                    'gui_scripts': ['unicodenames=unicodenames:main']})
