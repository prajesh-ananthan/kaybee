import kaybee

# Sphinx setup
project = 'Kaybee'
version = kaybee.__version__
release = version
master_doc = 'index'
exclude_patterns = ['_build']
extensions = ['sphinx.ext.intersphinx', 'alabaster', 'kaybee']
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('http://sphinx.pocoo.org', None),
    'dectate': ('http://dectate.readthedocs.io/en/latest', None),
}

# Theme setup
html_theme = 'alabaster'

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
    ]
}
