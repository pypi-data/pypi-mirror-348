# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['elimity_insights_client',
 'elimity_insights_client.api',
 'elimity_insights_client.api.entities']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.14,<10.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'simplejson>=3.17.6,<4.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'elimity-insights-client',
    'version': '10.2.1',
    'description': 'Client for connector interactions with an Elimity Insights server',
    'long_description': '# Elimity Insights Python client\n\nThis Python module provides a client for connector interactions with an Elimity\nInsights server.\n\n## Usage\n\n### Importing data to custom sources\n\nThe following snippet shows how to authenticate as a custom source and create a connector log at an Elimity Insights\nserver. You can generate a source identifier and token by visiting the custom source\'s detail page in Elimity Insights\nand clicking the \'GENERATE CREDENTIALS\' button, which can be found under the \'SETTINGS\' tab.\n\n```python3\nfrom datetime import datetime\n\nfrom elimity_insights_client import Client, Config, ConnectorLog, Level\n\nif __name__ == "__main__":\n    config = Config(id=1, url="https://local.elimity.com:8081", token="token")\n    client = Client(config)\n\n    timestamp = datetime.now()\n    log = ConnectorLog(level=Level.INFO, message="Hello world!", timestamp=timestamp)\n    logs = [log]\n    client.create_connector_logs(logs)\n```\n\n### Other API interactions\n\nThis module also provides a client for other API interactions with Elimity Insights. The snippet below shows how to\nauthenticate with an API token and list sources at an Elimity Insights server. You can generate a token identifier and\nsecret by visiting the \'API tokens\' page in Elimity Insights and clicking the \'CREATE API TOKEN\' button.\n\n```python3\nfrom elimity_insights_client.api import Config, sources\n\nif __name__ == "__main__":\n    config = Config(token_id="1", token_secret="my-secret-value", url="https://example.elimity.com", verify_ssl=True)\n    my_sources = sources(config)\n    print(my_sources)\n```\n\n## Installation\n\n```sh\n$ pip install elimity-insights-client\n```\n\n## Compatibility\n\n| Client version | Insights version |\n| -------------- | ---------------- |\n| 1              | 2.8 - 2.10       |\n| 2 - 3          | 2.11 - 3.0       |\n| 4              | 3.1 - 3.3        |\n| 5 - 6          | 3.4 - 3.5        |\n| 7              | 3.6 - 3.7        |\n| 8              | 3.8 - 3.15       |\n| 9              | ^3.16            |\n',
    'author': 'Elimity development team',
    'author_email': 'dev@elimity.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elimity-com/insights-client-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
