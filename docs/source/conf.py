import os
import sys
from datetime import datetime

# Add the python package to sys.path
sys.path.insert(0, os.path.abspath('../../python'))

project = 'ISETCam'
copyright = f'{datetime.now().year}, ISETCam'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_gallery.gen_gallery',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']

sphinx_gallery_conf = {
    'examples_dirs': os.path.abspath('../../python/tutorials'),
    'gallery_dirs': 'tutorials',
}

# Automatically generate API docs
def run_apidoc(app):
    from sphinx.ext.apidoc import main
    src_dir = os.path.abspath('../../python/isetcam')
    out_dir = os.path.abspath('api')
    main(['-f', '-o', out_dir, src_dir])

def setup(app):
    app.connect('builder-inited', run_apidoc)
