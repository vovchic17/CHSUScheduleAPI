import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(".."))
project = "CHSUScheduleAPI"
author = "VoVcHiC"
copyright = f"{date.today().year}, {author}"

templates_path = ["_templates"]
html_theme = "furo"
html_logo = "_static/logo.png"
html_css_files = ["extra.css"]
html_js_files = ["theme_modes.js"]
html_static_path = ["_static"]
todo_include_todos = True
html_show_sourcelink = False

ogp_site_url = "https://docs.chsutech.ru/en/latest/"
ogp_site_name = "CHSUScheduleAPI documentation"
ogp_description_length = 0
ogp_social_cards = {"image_mini": "_static/rtd.ico"}

extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx.ext.todo",
    "sphinxext.opengraph",
]
