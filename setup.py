from setuptools import setup, find_packages

setup(name='capture',
      version='1.0',
      package_dir={'': 'src'},
      author='Dan Bernstein',
      author_email='danbernstein94@gmail.com',
      packages=find_packages(include=['src']))
