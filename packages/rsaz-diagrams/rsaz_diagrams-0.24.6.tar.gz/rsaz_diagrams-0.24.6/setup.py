# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diagrams',
 'diagrams.alibabacloud',
 'diagrams.aws',
 'diagrams.azure',
 'diagrams.base',
 'diagrams.c4',
 'diagrams.custom',
 'diagrams.digitalocean',
 'diagrams.elastic',
 'diagrams.firebase',
 'diagrams.gcp',
 'diagrams.generic',
 'diagrams.ibm',
 'diagrams.k8s',
 'diagrams.oci',
 'diagrams.onprem',
 'diagrams.openstack',
 'diagrams.outscale',
 'diagrams.programming',
 'diagrams.saas',
 'resources']

package_data = \
{
    '': ['*'],
    'diagrams': ['*.png', '*.jpg', '*.svg', '*.ico', '*.json', '*.yaml', '*.yml', '*.txt', '*.md'],
    'resources': ['**/*.png', '**/*.jpg', '**/*.svg', '**/*.ico', '**/*.json', '**/*.yaml', '**/*.yml'],
}

install_requires = \
['graphviz>=0.13.2,<0.21.0', 'jinja2>=2.10,<4.0']

entry_points = \
{'console_scripts': ['diagrams = diagrams.cli:main']}

setup_kwargs = {
    'name': 'rsaz-diagrams',
    'version': '0.24.6',
    'description': 'Azure Extended version of diagrams',
    'long_description': '# diagrams-xtd\nExtended version of diagrams with some PR that never get merged and I want to use.\n\nMore details in [CHANGELOG](CHANGELOG.md). \n',
    'author': 'Diagrams-web',
    'author_email': 'no_spam@nowhere.mail',
    'maintainer': 'rajesh-ms',
    'maintainer_email': 'rajesh-ms@nowhere.mail',
    'url': 'https://github.com/rajesh-ms/diagrams',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
