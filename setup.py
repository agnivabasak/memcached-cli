from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        content = req.read()
        requirements = content.split('\n')
    return requirements

setup(
    name='memclid',
    version='1.0',
    author='Agniva Basak',
    author_email='agnivabasak1@gmail.com',
    packages=find_packages(), #finds packages in the '.' directory by default, ___init__.py used to indicate  that the directory should be treated as package
    include_package_data=True, #download all requirements of the package, user doesnt have to manaually do that
    install_requires=read_requirements(),
    entry_points='''
        [console_scripts]
        memclid=memclid.cli:cli
    ''' #since cli tool -> console_scritps, and memclid= means when you see command memclid look into memclid->cli.py->function cli
)