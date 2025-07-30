from setuptools import find_packages, setup

# Read requirements.txt and parse lines into a list
with open("/home/rptest/Desktop/carad-display/requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="carad-display",
    version="0.2",
    author_email='amgudym@mail.ru',
    description='A package for diplay of CARAD project, requires run on linux',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'carad-display = carad_display.main:main',
        ],
    },
    # data_files=
    #     ("/etc/systemd/system", "config/carad-display.service")
    # ,
    python_requires='>=3.11',
)