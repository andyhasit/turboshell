# Turboshell

*Turbocharge your shell with Python!*

## What is it?

Turboshell is a Python library which helps you do three things:

1. Generate shell commands from Python

2. Map commands to Python functions

3. Achieve superhuman productivity

If you're impressed with [ohmyz.sh](https://ohmyz.sh/), prepare to be blown away by **Turboshell**.

## Installation

Turboshell can generate ad hoc alias files (for specific servers, projects etc...) but the primary usage is managing your personal aliases, and that requires a bit of installation.

Don't worry, it's quick, unobtrusive, and easily removed. Just run this in your shell (bash or zsh):

```shell
$ sh -c "$(curl -fsSL https://raw.github.com/andyhasit/turboshell/master/install.sh)"
```

This will:

* Create a directory at a location of your choice, and dump a few files there.
* Create a virtual environment (optional but recommended).
* Add a line to your **.bashrc** or **.zshrc** file.

Alternatively see the [user guide]() for manual instructions.

## Quick start

There should now be two sub-directories in your **turboshell** directory:

* **/cmds** - the python files which you edit.
* **/shell** - the generated shell files which you don't edit.

Open **cmds/my_cmds.py** and make some changes:

```python
from turboshell import ts

ts.alias("test.1", "echo Testing 1", info="A simple alias")

@ts.cmd(alias="test.2", info="Calls a Python function")
def speak():
    print("Testing 2")
```

Then run:

```bash
$ ts.rebuild
```

This command does two things:

**1.** It rebuilds the **shell/definitions** file, where you can now see your aliases:

```bash
alias test.1='echo Testing 1'
alias test.2='turboshell cmds.my_cmds.speak'
```

**2.** It sources **shell/init**, which loads your new commands into the current shell session:

```bash
$ test.1
Testing 1
$ test.2
Testing 2
```

A quick peek at the files should give you a sense of how it works, if not read the details [here]().

#### Getting help

Run this command:

```bash
$ ts.help
```

You'll see a listing of available aliases. Note how `test.1` and `test.2` are listed in there too.

Note that you can use bash's built in `type` command to get more info:

```bash
$ type test.1
test.1 is aliased to `echo Testing 1'
$ type turboshell
turboshell is aliased to `bash /home/andrew/turboshell/build/turboshell'
```



#### About the dots

You're encouraged to use **.** as separators in your commands as:

* It looks neat!
* It avoids clashes.
* TAB completion makes it feels like typing code in an editor.
* Turboshell has a matcher which lets you partially type commands.

The matcher lets you type the first n letters of each words between the dots:

```bash
$ t.1      # Runs test.1
$ tes.2    # Runs test.2
$ t.in     # Runs ts.info
```

If it finds a unique match, it runs that command. If it finds multiple matches, it gives you an easy way to run the one you want:

```
$ g.s
Turboshell found multiple matches:

  1. git.show
  2. git.status

Run your choice with alias 'u' followed by the number, e.g.
> u 1
```

So if you wanted git status, you'd type:

```bash
$ u 2
```

Alternatively you could just type:

```bash
$ g.st
```

Which would only find one match, and therefore run it.



Order:

bash bad

long cmds

why would you do that?



If you are only typing one letter from each word you can also type it like this:

This comes in handy when you create longer aliases like:

```bash
$ projects.acme.backend.pytest
$ p.a.b.t
$ .pabt
```



This relies on bash's `command_not_found_handle` which you may already have customised. There is a section on this in the user guide. 

#### About bash

This doesn't work for commands like `cd` or `source` because of sub shells.



## How can I use it?

This section covers the three main points:

1. Generate aliases

2. Map aliases to Python

3. Unlock superhuman productivity 

There is also a more detailed [reference]() and some [recipes]().

### Generate bash aliases

> This section will alias `grep` command because it's
>
> are included in `turboshell.contrib.search` 

Instead of defining aliases one-by-one in your **bash_aliases** file:

```bash
alias grep.js="grep -ir $1 --include=\*.js"
alias grep.py="grep -ir $1 --include=\*.py"
```

You generate them using simple Python code:

```python
import turboshell as ts

for ext in ["js", "py"]:
    ts.alias(f"grep.{ext}", f"grep -ir $1 --include=\*.{ext}")
```

Generating aliases helps you do several things:

#### 1. Create permutations

You can easily tweak the code above to add case-sensitive permutations:

```bash
$ grep.js.cs
$ grep.py.cs
```

Hard coding options and permutations into the alias name saves time as:

* You don't have to remember syntax
* You don't have to type it in full

##### About typing commands

Your shell should have some form of auto completion enabled. You can also bind the `TAB` key to cycle through options by setting:

```bash
bind TAB:menu-complete
```

Which should enable this behaviour:

```bash
$ grep.             # hit TAB
$ grep.js           # hit TAB
$ grep.py           # hit TAB
$ grep.py.cs foo    # Type args and hit ENTER
```

##### About.the.dots

Auto complete doesn't treat `.` as a special character, but Turboshell uses it to find a command from the first **n** letters of each chunk.

You can run `grep.py.cs` by typing any of the following:

```bash
$ gr.p.c
$ g.py.c
$ g.p.c
```

If Turboshell finds multiple matches, it will ask you which one to run:

```bash
$ gr.p foo
Found 3 commands matching "gr.p": 
  0 - [Cancel]
  1 - grep.py
  2 - grep.py.
  3 - grep.py.cs
> Enter number:
> 2
grep.py.cs foo
```

If you're only specifying the first letter of each chunk (e.g. `g.p.c`) you can go even shorter:

```bash
$ .gpc
```

These functions are optional and can be controlled by  environment variables.

#### 2. Build messy commands

These days your `grep.js` alias might look more like this:

```bash
alias grep.js="grep -ir $1 --include=\*.js --include=\*.ts --include=\*.jsx --include=\*.tsx --exclude-dir=node_modules" 
```

That's a nightmare to maintain in an aliases file, but easy in Python:

```python
js_include = ["js", "ts", "jsx", "tsx"]
js_exclude = ["node_modules", "dist"]

inc_str = " ".join([f"--include=\*.{s}" for s in inc])
exc_str = " ".join([f"--exclude-dir={s}" for s in exc])

ts.alias("grep.js", "grep -ir $1 {inc_str} {exc_str}")
ts.alias("grep.js.cs", "grep -r $1 {inc_str} {exc_str}")
```

This seems like a lot of code to get `grep` commands, but we're just laying foundations for what's to come.

#### 3. Reuse settings

If you create aliases for the `find` command:

```bash
$ find.js
$ find.js.cs
$ find.py
$ find.py.cs
```

You could simply reuse `js_include` and `js_exclude`.

```python
find_ext = ' -o '.join([f'-name "*.{s}"' for s in js_include])
find_cmd = f'find . -type f -name "*$1*" \( {find_ext} \)'
ts.alias('find.js', find_cmd)
```

#### 4. Switch to functions

That last alias won't work because bash expands the variables, so you need to define it as a function instead, which is an easy switch:

```python
ts.func('find.js', find_cmd)
```

You can also generate multi-line functions:

```python
for service in ["web", "db"]:
    ts.func(
        f"kube.pod.{service}.bash",
        # The remaining arguments make up the function body
        f"POD=$(kubectl get pods | grep {service}- | cut -d' ' -f1)",
        "kubectl exec -it $POD -- bash"
    )
```

> The resulting command saves you having to copy and paste the pod name from one command to another.

This kind of alias save a lot of typing, and with Turboshell you save even more:

```bash
$ kube.pod.web.bash
$ k.p.w.b
$ .kpwb
```

### Map aliases to Python

Turboshell lets you easily point aliases to Python functions:

```python
@ts.cmd(alias="shout", args=["word", "times:int"])
def shout_n_times(word, times):
    for i in range(times):
    	print(word.upper())
```

Run `ts.rebuild` as before to load your new alias:

```bash
$ ts.rebuild
Generated 231 aliases in 1.406 ms
$ shout hello 3
HELLO
HELLO
HELLO
```

#### It's normal Python

It's normal Python, so you can do whatever you like:

* Connect to data sources
* Prompt for user input
* Launch a GUI

Turboshell runs that code in the virtual environment created during installation, so you can install libraries separately from your system Python.

There are some commands to help with that:

```bash
$ ts.venv.activate         # Activate the virtual env
$ ts.venv.deactivate       # Deactivate the virtual env
$ ts.pip.install foo       # Install a package in the virtual env
$ ts.pip.freeze            # Freeze the requirements
```

#### It's a normal alias

The resulting `shout` is a normal alias, so you can alias to it:

```python
for i in range(10):
    ts.alias(f"shout.{i}", f"shout $1 {i}")
```

You now have pre-populated aliases:

```bash
$ shout.3 hello    # alias to "shout hello 3"
HELLO
HELLO
HELLO
```

Don't worry, you can load 10,000 aliases in your shell in milliseconds without affecting anything other than your productivity.

#### Return to bash

You can also pass values back to bash, which is useful because 





### Unlock superhuman productivity

#### Get help

What's the point of creating aliases if you forget you have them or what they do?

```bash
$ ts.help
$ ts.info
```



#### Alias everything

* git.status
* web, exp, kill port 8000




```bash
$ git.show         # git show
$ git.status       # git status
$ exp              # launch your file explorer
$ web              # launch your browser
$ web.google foo   # launch browser at google.com/search?q=foo
backups
mkdir foo && cd "$_"
```

#### Use namespaces

A lot of people have very short aliases for frequently used commands:

```bash
alias gs="git status"
alias gl="git log"
alias gp="git push"
alias gcm="git commit"
alias gcp="git cherry-pick"
alias gaa="git add -A"
```

There are several problems with this:

1. You forget which aliases you created
2. You forget what they do
3. Letters mean different things (e.g. `p` could mean push, pick or patch)
4. They don't scale well to multiple permutations

With Turboshell you can create aliases with descriptive names:

```bash
alias git.status="git status"
alias git.log="git log"
alias git.commit="git commit"
alias git.cherry-pick="git cherry-pick"
alias git.add.all="git add -A"
```

But still type rather short commands:

```bash
$ g.l     # git log
$ g.sh    # git.show
$ g.st    # git.status   
```

You can very quickly see what commands exist in the namespace:

```bash
$ g.
```

And check what an alias is before running it:

```bash
$ g.c?
```

More complex commands will have an info string, which you can examine:

```bash
$ ts.info g.c
```

#### Use config files

Rather than generate the `grep` and `find` aliases from Python lists, you could generate the from config in a JSON file:

```python
{
    "js": {
         "exclude": ["node_modules", "dist"],
         "extensions": ["js", "ts", "jsx", "tsx"]
    },
    "py": {
         "exclude": ["venv"],
         "extensions": ["py"]
    }
}
```

The advantage of JSON is that we can modify it easily:

```python
FILE_CONFIG = "/path/to/search/config.json"

@ts.cmd(alias="search.config.add", args=["lang", "group", "value"])
def add_to_config(lang, group, value):
    with open(FILE_CONFIG) as fp:
        config = json.load(fp)
    if lang not in config:
    	config[lang] = {"exclude": [], "extensions": []}
    config[lang][group].append(value)
    with open(FILE_CONFIG, "w") as fp:
        json.dump(config, fp)
```

You could use the command like so:

```bash
$ search.config.add js extensions tsx
```

You then rebuild to see your new aliases:

```bash
$ ts.rebuild
```

But we can actually do better! First lets *name* the command rather than make it an *alias*:

```python
@ts.cmd(name="search.config.add", args=["lang", "group", "value"])
```

Now lets create an alias which will run that function, followed by `ts.rebuild`:

```python
ts.alias(
    "search.config.add", 
    "turboshell search.config.add $* && ts.rebuild"
)
```

Now our alias creates and updates aliases on the fly:

```bash
$ grep.css
Command not found
$ search.config.add.file_extension css css
$ grep.css foo    # grep in .css files
$ search.config.add.file_extension css scss
$ grep.css foo    # grep in .css and .scss files
```

You could also build permutations of that alias based on what's in the file:

```bash
$ search.config.js.add.file_extension jsx
$ search.config.js.add.exclude node_modules
$ search.config.js.remove.exclude.node_modules
```

That's maybe taking it a bit far, but just goes to show what it possible.

This lets you create commands specific to:

* Directories
* Projects
* Directories in projects
* Environments
* Clients
* Weekdays, years, dates etc...




#### Avoid changing directories

Changing directories saps time as:

1. You may need to think about where you are before you type
2. You may need to type long commands
3. You probably want to go back to where you were later
4. You probably keep a few terminal sessions open to avoid all this

You can drastically reduce the need to change directories (or keep tabs open) by making aliases which run in another directory and return to where you were:

```bash
alias projects.acme.git.status="cd /projects/acme && git status && cd -"
```

You could use it like this:

```
.pags
```

Use the config pattern, or just directory listings to generate aliases for every directory you cd to.

#### Use scoped alias files

avoid acme



* Generate alias files, direnv
* Copy to server



#### Create throw away commands



That's the basic usage. Turboshell does several other things which will 



#### Keep info at hand



You can of course pipe in and out of these functions, which makes it easy 

## Why use it?

#### Utility commands

Create aliases for the command options you use most, or might use:

```bash
$ grep.js foo  # Find js files with "foo" in text
$ find.js foo  # Find js files with "foo" in name
```

Aliases save you time by:

* Reducing typing (and typos) 
* Not having to look up a command's syntax rules

Generating aliases with code lets you:

* Manage permutations (e.g. case-sensitive versions of those)
* Build messy commands (e.g. make `grep` include ` js|ts|jsx|tsx`  extensions)
* Reuse data (e.g. make `find` use those same extensions)

#### Context commands

Create commands specific to your projects, directories, clients, environments, servers etc...

E.g. you're developing a website for client **Acme** and want the following:

```bash
$ acme.fe.git.status      # run "git status" in /projects/Acme/frontend
$ acme.be.git.status      # run "git status" in /projects/Acme/backend
$ acme.fe.tests           # run "npm tests" in /projects/Acme/frontend
$ acme.be.tests           # run "pytest" in /projects/Acme/backend
$ acme.live.ssh           # view logs on live server
$ acme.dev.ssh            # view logs on dev server
$ acme.live.ssh           # ssh to live server
$ acme.dev.ssh            # ssh to dev server
```

These aliases save even more time as you don't need to change directory.

Don't worry:

##### 1. You don't have to type

Instead of typing this:

```bash
$ acme.fe.git.status
```

You can just type the first letter(s) of each word:

```bash
$ a.f.g.s
```

And Turboshell will find the matching command or present you with a choice of matches.

You can also set up TAB completion so commands with `.` feel like typing in an IDE.

##### 2. Your shell can handle 1000's of aliases

Let's generate 10,000 aliases:

```python
for i in range(10000):
    ts.alias(f"test.{i}", f"echo testing {i}"
```

See how it rebuilds in milliseconds:

```bash
$ ts.rebuild 
Generated 10000 commands in 18.305 ms
```

These aliases don't impact your shell performance - in fact you won't even notice they exist.

##### 3. The code is really simple





* 

## What can I do with it?

#### Generate aliases

The following Python code:

```python
import turboshell as ts

ts.alias("grep.js", "grep -ir $1 --include=\*.js")
```

Will generate this alias:

```bash
alias grep.js="grep -ir $1 --include=\*.js"
```

Which you can use like so:

```bash
$ grep.js foo    # List all instances of "foo" in files with ending in .js
```

Aliases save time as:

* You type less (less typing = fewer typos = less re-typing)
* You don't have to look up command syntax
* You can combine commands into one

You should be creating as many as possible!

#### Reload

Turboshell comes with several built in aliases, the main one being:

```bash
$ ts.rebuild
```





You can also create aliases which point to Python functions, for example:

```python
@ts.cmd(alias="shout", arg="word")
def shout(word):
    print(word.upper())
```

Which

```bash
$ shout foo
FOO
```









Generates these two commands:

```bash
$ grep.js foo
main.js:function foo() {
dist/main.js:function foo() {
$ shout foo
FOO

### Why define aliases?

Aliases save time by:

1. Reducing the amount you type (and mistype/retype) 
2. Reducing the need to look up syntax rules.

### Why generate aliases?

Generating aliases with code is easy: you just build strings inside loops:

```python
for ext in ["js", "py"]:
    ts.alias(f"grep.{ext}", f"grep -ir $1 {ext}")
```

This lets you do several things:

#### Create permutations

Say we want grep commands for Python files, or case sensitive versions:

```bash
$ grep.js.ci
$ grep.js.cs
$ grep.py.ci
$ grep.py.cs
```

#### Build messy commands

Say we want multiple file extensions for our grep:

```bash
grep -ir foo --include=\*.js --include=\*.jsx --include=\*.ts --include=\*.tsx --exclude-dir=node_modules'
```

#### Create specific commands

You can loop through directories, lists of projects, or config files to create highly specific aliases.

```bash
$ acme.git.status
$ acme.tests.js
$ acme.tests.py
```

These aliases save even more time because you don't have to change directory.

You can use TAB completion like an IDE, or just type the first letter of each word:

```bash
$ acme.git.status
$ a.g.s
```

And Turboshell will find the correct command or prompt you to select.



* You can build these up from directory listings, config files, whatever you like.
* You can define 1000's of aliases



## 



In the Python module you define aliases like so:

```python
import turboshell as ts

ts.alias("grep.js", "grep -ir $1 --include=\*.js")
```

You then this command:

```bash
$ grep.js foo
```

> This will search for "foo" in .js files recursively.

That's the simplest. It does a whole lot more.



does three things:

* Loads a Python module in which you define aliases.
* Rebuilds the alias definitions file.
* Sources that file, making your new aliases instantly available.



Whenever you make changes to your Python 



 It will make you more productive than you thought was ever possible.

## How it works

Turboshell is a Python module which generates a text file with alias definitions.

One of those aliases is:

```bash
$ ts.rebuild
```

Which does three things:

* Loads a Python module in which you define aliases.
* Rebuilds the alias definitions file.
* Sources that file, making your new aliases instantly available.

You can also source that file from your **.bashrc** or **.zshrc** to make those aliases available in new shell sessions.

#### Defining aliases

Placing this code in your Python module:

```python
import turboshell as ts

for ext in ["js", "py"]:
    ts.alias(
        "grep.{}".format(ext),
        "grep -ir $1 --include=\*.{}".format(ext),
    )
```

Will result in these two aliases being created:

```bash
alias grep.js="grep -ir $1 --include=\*.js"
alias grep.py="grep -ir $1 --include=\*.py"
```

Which you can use like so:

```bash
$ grep.py foo   # search for "foo" in .py files
$ grep.js bar   # search for "bar" in .js files
```

#### Pointing aliases to Python

You can also point aliases to python functions:

```python
from simpleeval import simple_eval

@ts.cmd(alias="calc")
def calculator():
    while True:
        expr = input("> ")
        print(simple_eval(expr))
```

You now have an interactive calculator:

```bash
$ calc
> 21 + 19 / 7 + (8 % 3) ** 9
535.7142857142857
> 
```

The code runs inside virtual environment, so can install libraries (like [simpleeval](https://github.com/danthedeckie/simpleeval) we just used) without interfering with your system Python.

You can also specify arguments and return strings to bash, which lets you mix Bash and Python (more on this later).

Turboshell has several other tricks up its sleeve, but first let's take a step back.

## Shell productivity

### Why use aliases

Aliases save time in several ways:

##### You type less

Why type this:

```bash
$ grep -ir foo --include=\*.js
```
When you could type this:

```bash
$ grep.js foo
```

The problem is not just typing, but also mistyping, which is why we should minimise typing.

##### No need to remember syntax

You can bake syntax and options into the alias name, for example:

```bash
alias grep.js.cs="grep -r $1 --include=\*.js"
alias grep.js.ci="grep -ir $1 --include=\*.js"
```

The only time you need to look up syntax is when first defining them.

> You can use the TAB key to cycle through options.

##### You can combine commands

```bash
alias js.open="grep.js | ts.select | code"
```





### Why generate aliases



grep permutations

very simple code

the smaller the command the more likely to use it.

### Adding context

The real power of generating aliases

project git

### Bash functions

kubernetes



### Combining Bash and Python

Think of an example.





#### Comparison to  [ohmyz.sh](https://ohmyz.sh/)

* It works on bash, zshell and other shells.
* You decide what your aliases are called.
* You'll do a lot less typing.
* You can generate aliases specific to your projects and directories (which is **huge**).
* You can point aliases to Python code (who wants to write bash?)
* Plugins are just Python modules (which are a lot more powerful)

* It only deals with commands, not themes etc...

#### Comparison to [click](https://click.palletsprojects.com/)

Turboshell and click both have features for passing CLI args to Python functions, but they have totally different aims:

* Click helps you build a CLI tool in Python for wider circulation, and you typically need to activate a virtual environment before using the commands.
* Turboshell generates shell aliases specific to your system, projects, servers or environments. Some of those aliases may call Python functions, in which case the virtual environment is invisibly loaded.

Other cool things?

## Contributing

PRs welcome. Run tests with:

```
$ pytest
```

Please also run flake8.

Make sure it runs with python3.6 and bash.

## Licence

[MIT](https://opensource.org/licenses/MIT)





This installation is completely removable and doesn't affect your system.

The only prerequisite is Python 3.6 of above (for [f-strings](https://realpython.com/python-f-strings/)).

Create an empty directory (say **~/turboshell**) and run the following commands inside it:

```bash
python3 -m .venv                      # create a virtual env (however you like)
source .venv/bin/activate             # activate it
pip install turboshell                # install turboshell
python turboshell -m configure        # generate the initial files
source $PWD/generated/definitions     # load the definitions in current shell session
```

Check your installation with:

```bash
$ ts.info
```

The **cmds.py** file is where you will do your work.
