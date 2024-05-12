from datetime import date  # noqa: INP001

project = "CHSUScheduleAPI"
author = "VoVcHiC"
copyright = f"{date.today().year}, {author}"  # noqa: DTZ011, A001

templates_path = ["_templates"]
html_theme = "furo"
html_logo = (
    "https://raw.githubusercontent.com/vovchic17/static/main/src/logo.svg"
)
html_css_files = [
    "extra.css",
]
html_static_path = ["_static"]
todo_include_todos = True
extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx.ext.todo",
]
