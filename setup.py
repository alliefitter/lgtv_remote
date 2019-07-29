from setuptools import setup, find_packages


with open('./requirements.txt') as file_object:
    requirements = file_object.read().splitlines()

setup(
    name='lgtv_remote',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lgtv-remote = lgtv_remote.main:main'
        ]
    },
    url='',
    license='',
    author='Allie Fitter',
    author_email='afitter@cellcontrol.com',
    description='CLI that allows control over LG smart TVs.',
    install_requires=requirements
)
