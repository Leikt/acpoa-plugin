# ACPOA Builder
## What is ACPOA
ACPOA is the acronym for "Application Core for Plugin Oriented Applications". It's a tool to create flexible and extendable application.
It pronounces "ak poa".
## Create a plugin
In order to create a plugin from a directory, you will need python 3.9 (or more) installed. You should use a virtual environment
for your project.

### Plugin directory structure
Every project has a structure, ACPOA make no exception. Here is the base structure you should have :
```
<plugin_name>
    ├── LICENSE
    ├── plugin.cfg
    ├── README.md
    ├── setup.py
    ├── src
    │   └─── <plugin_name>
    │           ├── cfg/
    │           ├── data/
    │           ├── __init__.py
    │           └── <your_scripts>.py
    ├── tests
    └── venv
```
### New plugin assistance
If, like me, you are lazy, you can use the package *acpoa-plugin* to automatically create new plugin directory.
- Install the package : `python3 -m install acpoa-plugin`
- Create a new plugin directory with `python3 -m install acpoa-plugin new NAME [PATH] [OPTIONS] `. Where:
  - **NAME** is the name of the plugin
  - **PATH** is the directory where to create plugin.
  - Optional parameters:
    - `-p | --pretty-name "NAME"` specifies the pretty name of the plugin (default is the same as name)
    - `-l | --license FILE` specifies the license by filename (default LICENSE)
    - `-u | --url URL` specifies the main url of the project (default empty)
    - `-d | --description "TEXT"` specifies the short description of the project (default empty)
    - `-v | --version VALUE` specifies the plugin version (default 0.0.1)
    - `-a | --author 'NAME'` specifies the name of the author (you)
    - `-e | --author-email 'EMAIL'` specifies the author's email (yours)
    - `-f | --force` delete the existing directory if it exists then create a new one