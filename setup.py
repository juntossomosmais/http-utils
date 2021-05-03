# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['http_utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'urllib3>=1.26.4,<2.0.0']

setup_kwargs = {
    'name': 'http-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# This setup.py was autogenerated using poetry.