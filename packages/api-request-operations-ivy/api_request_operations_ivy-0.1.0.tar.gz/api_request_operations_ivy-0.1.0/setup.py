# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_request_operations_ivy']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=4.2.0,<5.0.0', 'pytest>=8.3.5,<9.0.0', 'requests>=2.32.3,<3.0.0']

setup_kwargs = {
    'name': 'api-request-operations-ivy',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Patrick White',
    'author_email': 'whitep@vcu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
