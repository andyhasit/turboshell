# Turboshell

*Turbocharge your shell with Python!*

## What does it do?

Turboshell lets you do two things:

#### 1. Generate shell aliases using python

The following code:

```python
from turboshell import ac

ac.alias('grep-py', 'grep -r --include=*.py')
ac.alias('grep-js', 'grep -r --include=*.js')
```

Results in these aliases:

```bash
alias grep-js='grep -r --include=*.js'
alias grep-py='grep -r --include=*.py'
```

Which you can use in the shell like so:

```bash
$ grep-py expr my-code-dir
```

This example is moot, but shifting this from a text file to Python you bring in for-loops, variables and all that. You can also document your aliases easily.

**Note:** You need to run `turboshell.rebuild` to see your new aliases appear - see installation.

#### 2. Write shell commands in Python

The following code:

```python
from turboshell import ac

langs = {'FR': 'Bonjour', 'ES': 'Hola', 'EN': 'Hello'}

def say_hello(lang, name):
    print('{} {}!'.format(langs[lang], name))

# Regitser function as a turboshell command
ac.cmd(say_hello)

# Create alises:
ac.alias('hello', 'turboshell say_hello EN')
ac.alias('hello-spanish', 'turboshell say_hello ES')
ac.alias('hello-french', 'turboshell say_hello FR')
```

Results in these aliases:

```bash
alias hello='turboshell say_hello'
alias hello-spanish='turboshell say_hello ES'
alias hello-french='turboshell say_hello FR'
```

Which you can use in the shell like so:

```bash
$ hello Mike
Hello Mike!
$ hello-french Anabelle
Bonjour Anabelle!
```

You don't *need* Turboshell to point an alias to a Python script. Turboshell just automates the wiring for you (reloading, handling args, virtual environments etc...) so you can do it in a snap.

## How does that help me?

#### 1. Productivity

Aliases let you type commands faster, with less typos and without having to remember all the arguments. Generally, the more commands you can replace with aliases, the faster you can work.

The difficulty is:

1. Managing a large numbers of aliases in text files is rather clunky.
2. Its easy to forget what aliases you created and how to use them.

By generating aliases with code rather than managing them in a text file, it becomes easy to maintain large sets of similar aliases, and generally organise them better. There is also a feature for adding documentation accessible from the command line.

You can also derive these aliases from sets of projects, clients, weekdays, servers etc... You can regenerate your aliases with a single command whenever those lists change.

> Your shell can load 1000s of aliases in milliseconds without any kind of lag.

#### 2. Solve problems quicker

Ever get stuck trying to pipe 3 commands with crazy arguments together to produce a result?

With Turboshell you can bind an alias to a Python function in under 10 seconds. Effectively this means you can replace problematic parts of a command chains with python functions.

#### 3. Write more useful commands

Once you have a mechanism in place which lets you quickly create new shell commands with the full power of python and all its libraries behind you, you will hopefully be tempted to write more and more useful commands for the kind of work you do.

With Python you can:

* Work with files and directories (locally or over ssh using [paramiko](http://docs.paramiko.org/en/stable/api/client.html))
* Pipe in and out of other commands using [subprocess](https://docs.python.org/3/library/subprocess.html)
* Connect to APIs using [requests](https://requests.readthedocs.io/en/master/)
* Scrape from web pages using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Your imagination is the only limit!

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

````bash
pip install virtualenv
virtualenv -p python3 ~/turboshell/virtualenv  # or wherever you want to create it
```

Do this even if you use **pyenv** or other such tool for managing your virtual environment. 

This virtual environment will only be activated:

- When running the turboshell command*
- When installing packages used for your commands

\* This is done automatically, and only for the scope of the command. Turboshell commands won't affect (or use) whatever virtual environment you may have active.

##### 3. Install turboshell

Activate your virtual environment:

```bash
source ~/turboshell/virtualenv/bin/activate
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
~/turboshell $

  ---------------------------------
  TURBOSHELL SUCCESSFULLY INSTALLED
  ---------------------------------

  Add the following line to your shell initialisation file (e.g. ~/.bashrc or ~/.zshrc)

     source '/home/andrew/turboshell/generated/definitions'

  This will load your aliases into new shell sessions.
  To load them into this shell session just run the above command at the prompt.
  You should then be able to run:

      turboshell.info

~/turboshell $
```

Follow these instructions. If you ever move your turboshell directory, just run step 4 again.

## Contributing

PRs welcome. Please run flake8. 

If you're thinking of rewriting this using decorators, you'll get stung.