from setuptools import find_packages
from setuptools import setup

setup(name='scraps',
      version='0.1',
      description='_scraps',
      url='',
      author='Vito De Tullio',
      author_email='vito.detullio@gmail.com',
      license='GPL3',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'marshmallow-dataclass[enum,union]',
          'pydantic'
      ],
      entry_points={
          'console_scripts': [
              'mm=mm:main',
              'executable=executable:main',
              'pd=pd:main'
          ],
          'gui_scripts': [
              'unicodenames=unicodenames:main'
          ],
      })
