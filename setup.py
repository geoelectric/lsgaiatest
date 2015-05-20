# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.realpath(__file__))
requirements = os.path.join(here, 'requirements.txt')
with open(requirements) as f:
    required = f.read().splitlines()

setup(
    name='lsgaiatest',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lsgaiatest = lsgaiatest.cmd:main'
        ]
    },

    install_requires=required,

    author='Geo Mealer',
    author_email='gmealer@mozilla.com',
    description='List what tests gaiatest would run for a given set of options.',
    url='https://github.com/geoelectric/lsgaiatest',
    license='MPL 2.0',
    keywords='gaia gaiatest marionette test list ls',
)
