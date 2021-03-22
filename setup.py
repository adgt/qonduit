from __future__ import print_function
from setuptools import setup, find_packages
import os
from os.path import join as pjoin
from distutils import log

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)

here = os.path.dirname(os.path.abspath(__file__))

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

name = 'qonduit'
LONG_DESCRIPTION = 'A Python library with visualization tools and workflows for quantum computing that utilize the best of what’s available. Can be used in Jupyter notebooks, JupyterLab, and the IPython kernel.'

# Get pulsemaker version
version = get_version(pjoin(name, '_version.py'))

setup_args = dict(
    name=name,
    version=version,
    description='A Python library with visualization tools and workflows for quantum computing',
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    install_requires=[
        'ipywidgets>=7.0.0',
    ],
    packages=find_packages(),
    zip_safe=False,
    author='Amir Ebrahimi',
    author_email='github@aebrahimi.com',
    url='https://github.com/adgt/qonduit',
    keywords=[
        'ipython',
        'jupyter',
        'widgets',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

setup(**setup_args)
