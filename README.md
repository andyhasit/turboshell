# Turboshell

*Turbocharge your shell with Python!*

## What does it do?

Turboshell is a *tool* which lets you do two things:

#### 1. Generate shell aliases using python

The following code:

```python
from turboshell import ac

for ext in ['py', 'js']:
    ac.alias(
        'grep-{}'.format(ext), # the alias 
        'grep -r --include=*.{}'.format(ext) # the command
    )
```

Results in these aliases:

```bash
alias grep-js='grep -r --include=*.js'
alias grep-py='grep -r --include=*.py'
```

Which you can use in the shell like so:

```bash
$ grep-py expr /path/to/files
```

There is also an option to add info to aliases (see further down).

#### 2. Write shell commands in Python

The following code:

```python
from turboshell import ac

langs = {'FR': 'Bonjour', 'ES': 'Hola', 'EN': 'Hello'}

def say_hello(args):
    lang, name = args
    print('{} {}!'.format(langs[lang], name))

ac.cmd(say_hello) # Registers a function as a turboshell command

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

By generating aliases with code rather than working directly with a text file, it becomes easy to maintain large sets of similar aliases, and generally organise them better.

You can build sets aliases with data embedded for lists projects, clients, weekdays, servers etc...

```bash
cd.project1                        # cd to wherever project1 is
log-time.wednesday.project2 2:20   # log 2h20m to project2 for Wednesday
ssh.client2.live                   # ssh into whatever client2's live server is
weather.thursday                   # print weather for Thursday
```

You get the idea. Its quicker to hit tab than to full type out args, so the more you can do this, the better. 

Ps: your shell can load 1000s of aliases in milliseconds without any kind of lag.

#### 2. Solve problems quicker

Ever get stuck trying to pipe 3 commands with crazy arguments together to produce a result?

With Turboshell you can bind an alias to a Python function in under 10 seconds. Effectively this means you can replace problematic parts of a command chains with python functions, and get the right result quicker.

#### 3. Write more useful commands

Once you have a mechanism in place to:

1. Quickly create new shell commands 
2. Generate sets of aliases for those

You will hopefully be tempted to write more and more useful commands for the kind of work you do.

You have the full power of python and all its libraries behind you, so you can make commands which:

* Work with files and directories (locally or over ssh using [paramiko](http://docs.paramiko.org/en/stable/api/client.html))
* Pipe in and out of other commands using [subprocess](https://docs.python.org/3/library/subprocess.html)
* Connect to APIs using [requests](https://requests.readthedocs.io/en/master/)
* Scrape from web pages using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Your imagination is the only limit! Your command library will also have its own virtual environment.

## How does it work?

Once you've installed it (see **Installation** below) you get the following command in your shell:

##### turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see **Manual** below).

##### turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your **scripts** module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your **.bashrc** file (or equivalent) which ensures these aliases are available in new shell sessions.

##### turboshell.reload

This is just an alias for `source /path/to/generated/alias/file`. Use this command if you called `turboshell.rebuild` in another shell session and want to reload the new aliases into the current session.

##### turboshell  cmd-name  [args]

This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
2. Load all the Python code in your **scripts** module
3. Find the function which you registered with the same name.
4. Call that function, passing the command line arguments as a list of strings.

## Manual

### Scripts

TODO: flesh out.

### Commands

You create a command (i.e. make it callable with `turboshell cmd-name`) by defining a function and passing it to `ac.cmd()`. Note that the function must take a single parameter which will be a list of strings.

```python
def say_hello(args):
    pass

ac.cmd(say_hello)
```

This registers the function using its name. If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

```python
ac.cmd(say_hello, name='my-hello-cmd')
```

The name is usually not so relevant as you will create an alias for it.

### Aliases

You create aliases to shell commands like so:

```python
ac.alias('grep-py', 'grep -r --include=*.{py}')
```

To create an alias for a command defined in turboshell, simply set the command to `turboshell cmd-name`:

```python
ac.alias('hello', 'turboshell say_hello')
ac.alias('hello-spanish', 'turboshell say_hello ES')
```

Just like normal aliases, you can preset some parameters in the alias if your function handles them:
```python
ac.alias('hello-spanish', 'turboshell say_hello ES')
ac.alias('hello-spanish', 'turboshell say_hello FR')
```


You can also creating an alias without parameters at the same time as passing a command.

```python
ac.cmd(say_hello, 'hello')
```

### Info

The `turboshell.info` command prints something like this:

```
  turboshell.info    | Shows info on commands
  turboshell.rebuild | Rebuilds and reloads the aliases in current shell
  turboshell.reload  | Reloads the aliases in current shell
```

You can add items in there by providing an extra string to `ac.alias()`:

```python
ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')
```

Or if declaring the alias directly in the call to `ac.cmd()`:

```python
ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')
```

Note that for `cmd()` the info is only used if alias is specified. The signature of `cmd` is:

```python
def cmd(self, function, alias=None, info=None, name=None):
    pass
```

You must provide arguments in the correct sequence, or specify keyword args as Python's [rules](https://realpython.com/python-kwargs-and-args/):

```python
ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')
```

Finally, you may explicitly add info entries separately from aliases:

```python
ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')
```

This is useful for aliases which have many permutations. 

### Arguments

TODO: flesh out (and provide decorators)

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
  ---------------------------------
  TURBOSHELL SUCCESSFULLY INSTALLED
  ---------------------------------

  Add the following line to your shell initialisation file (e.g. ~/.bashrc or ~/.zshrc)

     source '/home/andrew/turboshell/generated/definitions'

  This will load your aliases into new shell sessions.
  To load them into this shell session just run the above command at the prompt.
  You should then be able to run:

      turboshell.info

```

Follow these instructions. If you ever move your turboshell directory, just run step 4 again.

## Contributing

PRs welcome. Please run flake8. 

If you're thinking of rewriting this using decorators, you'll get stung.

## Licence

[MIT](https://opensource.org/licenses/MIT)