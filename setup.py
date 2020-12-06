from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='pyfenstein3d',
      version='1.0',
      description='Projeto de estudo reproduzindo jogo Wolfenstein3d utilziando técnica Raycasting',
      long_description=readme,
      license=license,
      author='Allison GrrriiiM',
      author_email='allison.f.oliveira@hotmail.com',
      url='https://github.com/GrrriiiM/pyfenstein3d',
      packages=[],
      )
