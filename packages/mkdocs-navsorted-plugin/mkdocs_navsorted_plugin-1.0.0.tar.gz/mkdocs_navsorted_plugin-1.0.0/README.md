# mkdocs-navsorted-plugin

https://github.com/idlesign/mkdocs-navsorted-plugin

[![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-navsorted-plugin)](https://pypi.python.org/pypi/mkdocs-navsorted-plugin)
[![License](https://img.shields.io/pypi/l/mkdocs-navsorted-plugin)](https://pypi.python.org/pypi/mkdocs-navsorted-plugin)
[![Coverage](https://img.shields.io/coverallsCoverage/github/idlesign/mkdocs-navsorted-plugin)](https://coveralls.io/r/idlesign/mkdocs-navsorted-plugin)
[![Docs](https://img.shields.io/readthedocs/mkdocs-navsorted-plugin)](https://mkdocs-navsorted-plugin.readthedocs.io/)

## Description

*mkdocs plugin to get nav sorted without yml directives*

Use numeric prefixes for your documentation files/directories names
to drive navigation items sort order.


Normal layout:
```
docs
|- section_a
|   |- file1.md
|   |- file2.md
|- section_b
|   |- file3.md
|   |- file4.md
|- about.md
|- index.md
|- quickstart.md
```

We turn into a prefixed one:
```
docs
|- 01_index.md
|- 10_quickstart.md
|- 20_section_a
|   |- 10_file2.md
|   |- 20_file1.md
|- 30_section_b
|   |- file3.md
|   |- file4.md
|- 40_about.md
```

So the navigation with this plugin would become:
```
index
quickstart
section_a
  file2
  file1
section_b
  file3
  file4
about
```

Read the documentation.

## Documentation

https://mkdocs-navsorted-plugin.readthedocs.io
