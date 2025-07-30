import kafka_async

project = 'kafka-async'
copyright = '2024, Timofei Kukushkin'
author = 'Timofei Kukushkin'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'myst_parser',
]
version = release = kafka_async.__version__

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ['_static']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'confluent_kafka': ('https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html', None),
}

autoclass_content = 'both'
autodoc_member_order = 'bysource'
autodoc_preserve_defaults = True
