import setuptools


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='pyfenstein3d',
                 version='1.1',
                 description='Projeto realizado em python com intuido educacional de tentar reproduzir o jogo Wolfenstein 3d no prompt de comando.',
                 long_description=readme,
                 license=license,
                 author='Allison GrrriiiM',
                 author_email='allison.f.oliveira@hotmail.com',
                 url='https://github.com/GrrriiiM/pyfenstein3d',
                 packages=setuptools.find_packages(exclude=["tests"]),
                 package_data={'pyfenstein3d': ['imgs/*.*', 'maps_pattern/*.*']},
                 install_requires=install_requires,
                 include_package_data=True,
                 )
