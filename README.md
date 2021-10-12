# Turboshell

*Turbocharge your shell with Python!*

## What does it do?

Turboshell makes it easy to:

1. Generate shell aliases
2. Write commands in Python

## Example

Once installed, you can write code like this in a Python file:

```python
from turboshell import ts

# Create a normal shell alias:
ts.alias('grep.js', 'grep -r --exclude-dir=node_modules --include=*.js')

# Create a turboshell command, and give it an alias:
@ts.cmd(alias='hello', positional=['name!'])
def say_hello(name):
    print('Hello ' + name)
```

Back in your shell run:

```bash
$ ts.rebuild
```

You will now have two new aliases available in your current (and any new) shell session:

```bash
$ grep.js
[results of grep...]
$ hello Joe
Hello Joe
```

The `grep.js` alias just points to the shell's `grep` command with options preset, its a normal alias.

The `hello` alias on runs our python function within a virtual environment, checking and passing arguments to it.

#### Similar tools

This may look a bit like [click](https://palletsprojects.com/p/click/) or [invoke](), but there's a difference. To call a command created with either of those you need to:

1. cd to the right directory
2. Activate the right virtual environment
3. Type something ugly like `python hello.py --name Joe`

Turboshell on the other hand installs a command which does all this for you. You simply pass the name of your command and any arguments:

```bash
$ turboshell say_hello Joe
```

You can also create an even shorter alias at the point of defining the command, or after.



commands like that too a similar manner , but the assumption is that you are actually trying to be productive and want to be able to call your commands with as little typing as possible.

Turboshell on the other hand assumes you want a permanent shell alias for the commands you write.

With Turboshell you can type the alias from any directory. The virtual environment is loaded invisibly (and doesn't touch any virtual environment you have active when calling the command).

Click and invoke are tools for creating powerful command interfaces.

Turboshell has a different goal to click or invoke: productivity in the shell.

## Why generate shell aliases?

Aliases make us more productive by reducing the number of arguments we have to type (or even remember):


```bash
$ grep -r --exclude-dir=node_modules --include=*.js hello
...vs
$ grep.js hello
```

You can also create aliases which combine commands, e.g. print the git status of another project without changing directory:

```bash
$ alias gitstat.project1='cd /path/to/project1 && git status && cd -'
```

With a bit of imagination, you'll find there are 100s of individual aliases you could create to make you more productive in the shell.

But creating aliases like these for every combination of file we might want to grep, or every git repository on our machine, is a lot of work.

Turboshell makes it trivially easily generate sets of aliases based on lists of projects, clients, directories, user names, email accounts, servers, weekdays, etc...

## Why write commands in python?

What if you want combinations of file extensions for your grep alias?

```bash
grep.py
grep.css
grep.js-html
grep.js-html-css
```

That's clearly going to get messy. Better create a command which accepts the file extension(s) as a first argument, let's call it **gerp**:

```bash
$ gerp js hello             # search js files only
$ gerp js-html-css hello    # search all js, html and css files
```

For this to work, our command must convert the first arg to grep syntax, which differs according to whether we specify one or more file types:

```
"gerp js"        >>   "grep -r --include=*.js"
"gerp js-html"   >>   "grep -r --include=*.{js,html,css}""
```

This is really basic string manipulation, but give this a try in bash script, and then in Python. Then add some validation. Then a unit test. Then use the same list of file types for a different command...

Writing commands in Python instead of bash is not only a hell of a lot easier, but you have the full power of Python's libraries at your fingertips:

* Work with files and directories...
* Work with csv, json, databases, spreadsheets...
* Call other shell commands with subprocess
* Do things over ssh using [paramiko](http://docs.paramiko.org/en/stable/api/client.html)
* Work with git repositories using [gitpython](https://gitpython.readthedocs.io/en/stable/index.html)
* Connect to APIs using [requests](https://requests.readthedocs.io/en/master/)
* Scrape from web pages using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* etc...

## Installation

##### 1. Create a directory for your Python scripts

Put this wherever you like, e.g.

```bash
mdkir ~/turboshell
```

Turboshell will create the following subdirectories:

* **scripts** - where you place your commands
* **generated** -  where turboshell places its generated files

##### 2. Create a virtual environment

Do this how you like. I recommend [installing virtualenv](https://docs.python-guide.org/dev/virtualenvs/) and typing:

```bash
pip install virtualenv
virtualenv -p python3 ~/turboshell/virtualenv  # or wherever you want to create it
```

Do this even if you use **pyenv** or other such tool for managing your virtual environment. 

This virtual environment will only be activated:

- When running a turboshell command\*
- When installing packages used for your commands

\* This is done automatically, and only for the scope of the command. Turboshell commands won't affect (or use) whatever virtual environment you may have active.

##### 3. Install turboshell

Activate your virtual environment:

```bash
source ~/turboshell/virtualenv/bin/activtooate
```

And either run:

```bash
pip install turboshell
```

Or, clone/download this repo and run:

```bash
pip install -e /path/to/repo
```

##### 4. Configure turboshell

With your virtual environment active, go to the directory you created in step 1 and run:

```bash
cd turboshell
python turboshell -m configure
```

You should see some output which looks like this:

```
  ---------------------------------
  TURBOSHELL SUCCESSFULLY INSTALLED
  ---------------------------------

  Add the following line to your shell initialisation file (e.g. ~/.bashrc or ~/.zshrc)

     source '/home/andrew/turboshell/generated/definitions'

  This will load your aliases into new shell sessions.
  To load them into this shell session just run the above command at the prompt.
  You should then be able to run:

      ts.info

```

Follow the printed instructions. If you ever move your turboshell directory, just run step 4 again.

## User Guide

See [USER_GUIDE.md](./USER_GUIDE.md).

## Contributing

PRs welcome. Run tests with:

```
$ py.test
```

Please also run flake8.

## Licence

[MIT](https://opensource.org/licenses/MIT)

