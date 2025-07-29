# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_storage_operations_ivy']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=4.2.0,<5.0.0',
 'psycopg-c>=3.2.7,<4.0.0',
 'psycopg2-binary>=2.9.10,<3.0.0',
 'psycopg[binary,pool]>=3.2.7,<4.0.0',
 'pytest>=8.3.5,<9.0.0',
 'structlog>=25.2.0,<26.0.0']

setup_kwargs = {
    'name': 'sql-storage-operations-ivy',
    'version': '1.0.0',
    'description': 'SQL Storage Middleware for SQLite and Postgres',
    'long_description': 'None',
    'author': 'Patrick White',
    'author_email': 'whitep@alumni.vcu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
