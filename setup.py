from setuptools import setup

setup(name='pysms',
      version='0.1',
      description='Python SMS Module for SIM900',
      url='https://github.com/argandas/pysms',
      author='Hugo Arganda',
      author_email='hugo.arganda@gmail.com',
      license='MIT',
      packages=['pysms'],
      install_requires=[
          'pyserial',
      ],
      zip_safe=False
      )
