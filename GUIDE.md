# Turboshell User Guide










Manual

Scripts

TODO: flesh out.

Commands

You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

    def say_hello(args):
        pass
    
    ac.cmd(say_hello)

This registers the function using its name, so you can invoke it like this:

    $ turboshell say_hello

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

    ac.cmd(say_hello, name='my-hello-cmd')

The name is usually not so relevant as you typically create aliased for these command.

Aliases

You create aliases to shell commands like so:

    ac.alias('grep-py', 'grep -r --include=*.{py}')

To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

    ac.alias('hello', 'turboshell say_hello')
    ac.alias('hello-spanish', 'turboshell say_hello ES')

Just like normal aliases, you can preset some parameters in the alias if your function handles them:

    ac.alias('hello-spanish', 'turboshell say_hello ES')
    ac.alias('hello-spanish', 'turboshell say_hello FR')

You can also creating an alias without parameters at the same time as passing a command.

    ac.cmd(say_hello, 'hello')

Info

The turboshell.info command prints something like this:

      turboshell.info    | Shows info on commands
      turboshell.rebuild | Rebuilds and reloads the aliases in current shell
      turboshell.reload  | Reloads the aliases in current shell

You can add items in there by providing an extra string to ac.alias():

    ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

Or if declaring the alias directly in the call to ac.cmd():

    ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

    def cmd(self, function, alias=None, info=None, name=None):
        pass

You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

    ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

Finally, you may explicitly add info entries separately from aliases:

    ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

This is useful for aliases which have many permutations. 

Arguments

TODO: flesh out (and provide decorators)



How does it work?

Once you've installed it (see Installation below) you get the following command in your shell:

turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your scripts module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

turboshell.reload

This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

turboshell  cmd-name  [args]







Manual

Scripts

TODO: flesh out.

Commands

You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

    def say_hello(args):
        pass
    
    ac.cmd(say_hello)

This registers the function using its name, so you can invoke it like this:

    $ turboshell say_hello

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

    ac.cmd(say_hello, name='my-hello-cmd')

The name is usually not so relevant as you typically create aliased for these command.

Aliases

You create aliases to shell commands like so:

    ac.alias('grep-py', 'grep -r --include=*.{py}')

To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

    ac.alias('hello', 'turboshell say_hello')
    ac.alias('hello-spanish', 'turboshell say_hello ES')

Just like normal aliases, you can preset some parameters in the alias if your function handles them:

    ac.alias('hello-spanish', 'turboshell say_hello ES')
    ac.alias('hello-spanish', 'turboshell say_hello FR')

You can also creating an alias without parameters at the same time as passing a command.

    ac.cmd(say_hello, 'hello')

Info

The turboshell.info command prints something like this:

      turboshell.info    | Shows info on commands
      turboshell.rebuild | Rebuilds and reloads the aliases in current shell
      turboshell.reload  | Reloads the aliases in current shell

You can add items in there by providing an extra string to ac.alias():

    ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

Or if declaring the alias directly in the call to ac.cmd():

    ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

    def cmd(self, function, alias=None, info=None, name=None):
        pass

You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

    ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

Finally, you may explicitly add info entries separately from aliases:

    ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

This is useful for aliases which have many permutations. 

Arguments

TODO: flesh out (and provide decorators)



How does it work?

Once you've installed it (see Installation below) you get the following command in your shell:

turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your scripts module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

turboshell.reload

This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

turboshell  cmd-name  [args]

This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
2. Load all the Python code in your scripts module
3. Find the function which you registered with the same name.
4. Call that function, passing the command line arguments as a list of strings.











Manual

Scripts

TODO: flesh out.

Commands

You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

    def say_hello(args):
        pass
    
    ac.cmd(say_hello)

This registers the function using its name, so you can invoke it like this:

    $ turboshell say_hello

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

    ac.cmd(say_hello, name='my-hello-cmd')

The name is usually not so relevant as you typically create aliased for these command.

Aliases

You create aliases to shell commands like so:

    ac.alias('grep-py', 'grep -r --include=*.{py}')

To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

    ac.alias('hello', 'turboshell say_hello')
    ac.alias('hello-spanish', 'turboshell say_hello ES')

Just like normal aliases, you can preset some parameters in the alias if your function handles them:

    ac.alias('hello-spanish', 'turboshell say_hello ES')
    ac.alias('hello-spanish', 'turboshell say_hello FR')

You can also creating an alias without parameters at the same time as passing a command.

    ac.cmd(say_hello, 'hello')

Info

The turboshell.info command prints something like this:

      turboshell.info    | Shows info on commands
      turboshell.rebuild | Rebuilds and reloads the aliases in current shell
      turboshell.reload  | Reloads the aliases in current shell

You can add items in there by providing an extra string to ac.alias():

    ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

Or if declaring the alias directly in the call to ac.cmd():

    ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

    def cmd(self, function, alias=None, info=None, name=None):
        pass

You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

    ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

Finally, you may explicitly add info entries separately from aliases:

    ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

This is useful for aliases which have many permutations. 

Arguments

TODO: flesh out (and provide decorators)



How does it work?

Once you've installed it (see Installation below) you get the following command in your shell:

turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your scripts module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

turboshell.reload

This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

turboshell  cmd-name  [args]

This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
2. Load all the Python code in your scripts module
3. Find the function which you registered with the same name.
4. Call that function, passing the command line arguments as a list of strings.



This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
2. Load all the Python code in your scripts module
3. Find the function which you registered with the same name.
4. Call that function, passing the command line arguments as a list of strings.


$ gerp js hello             # search js files only
$ gerp js-html-css hello    # search all js, html and css files
$ gerp * hello              # search all file extensions
```

For this, we need our **gerp** command to process our extension string to what grep expects:

```
js        >>     --include=*.js
js-html   >>     --include=*.{js,html,css}
```

You can attempt this in bash if you like (good luck) or you can write the logic in Python:

​```python








Manual

Scripts

TODO: flesh out.

Commands

You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

    def say_hello(args):
        pass
    
    ac.cmd(say_hello)

This registers the function using its name, so you can invoke it like this:

    $ turboshell say_hello

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

    ac.cmd(say_hello, name='my-hello-cmd')

The name is usually not so relevant as you typically create aliased for these command.

Aliases

You create aliases to shell commands like so:

    ac.alias('grep-py', 'grep -r --include=*.{py}')

To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

    ac.alias('hello', 'turboshell say_hello')
    ac.alias('hello-spanish', 'turboshell say_hello ES')

Just like normal aliases, you can preset some parameters in the alias if your function handles them:

    ac.alias('hello-spanish', 'turboshell say_hello ES')
    ac.alias('hello-spanish', 'turboshell say_hello FR')

You can also creating an alias without parameters at the same time as passing a command.

    ac.cmd(say_hello, 'hello')

Info

The turboshell.info command prints something like this:

      turboshell.info    | Shows info on commands
      turboshell.rebuild | Rebuilds and reloads the aliases in current shell
      turboshell.reload  | Reloads the aliases in current shell

You can add items in there by providing an extra string to ac.alias():

    ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

Or if declaring the alias directly in the call to ac.cmd():

    ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

    def cmd(self, function, alias=None, info=None, name=None):
        pass

You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

    ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

Finally, you may explicitly add info entries separately from aliases:

    ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

This is useful for aliases which have many permutations. 

Arguments

TODO: flesh out (and provide decorators)



How does it work?

Once you've installed it (see Installation below) you get the following command in your shell:

turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your scripts module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

turboshell.reload

This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

turboshell  cmd-name  [args]

This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
2. Load all the Python code in your scripts module
3. Find the function which you registered with the same name.
4. Call that function, passing the command line arguments as a list of strings.


def convert_exts(exts):
    if '-' in exts:
        exts = exts.replace('-', ',')
        return '--include=*.{' + exts + '}'
    return = '--include=*.' + exts
```

We can then slot it into a turboshell command which calls grep from Python:

```python
from turboshell import ts, call

@cmd(['exts', 'expr', 'path?'], alias='gerp')
def grep_cmd(exts, expr, path='.'):
    include_part = convert_exts(exts)
    cmd = 'grep -r {} --color=auto {} {}'.format(include_part, expr, path)
    call(cmd)
```

 We just run:

```bash
$ turboshell.rebuild
```

And we have an alias called **gerp** which calls our python function!





The `--color=auto` bit is required to preserve output colors.



Once you have this system in place, its easy to create 1000s of aliases based on any list:

* Projects
* Clients
* Servers
* Significant directories
* Days of the week
* etc...

Here's an example:

```python








Manual

Scripts

TODO: flesh out.

Commands

You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

    def say_hello(args):
        pass
    
    ac.cmd(say_hello)

This registers the function using its name, so you can invoke it like this:

    $ turboshell say_hello

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

    ac.cmd(say_hello, name='my-hello-cmd')

The name is usually not so relevant as you typically create aliased for these command.

Aliases

You create aliases to shell commands like so:

    ac.alias('grep-py', 'grep -r --include=*.{py}')

To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

    ac.alias('hello', 'turboshell say_hello')
    ac.alias('hello-spanish', 'turboshell say_hello ES')

Just like normal aliases, you can preset some parameters in the alias if your function handles them:

    ac.alias('hello-spanish', 'turboshell say_hello ES')
    ac.alias('hello-spanish', 'turboshell say_hello FR')

You can also creating an alias without parameters at the same time as passing a command.

    ac.cmd(say_hello, 'hello')

Info

The turboshell.info command prints something like this:

      turboshell.info    | Shows info on commands
      turboshell.rebuild | Rebuilds and reloads the aliases in current shell
      turboshell.reload  | Reloads the aliases in current shell

You can add items in there by providing an extra string to ac.alias():

    ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

Or if declaring the alias directly in the call to ac.cmd():

    ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

    def cmd(self, function, alias=None, info=None, name=None):
        pass

You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

    ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

Finally, you may explicitly add info entries separately from aliases:

    ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

This is useful for aliases which have many permutations. 

Arguments

TODO: flesh out (and provide decorators)



How does it work?

Once you've installed it (see Installation below) you get the following command in your shell:

turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your scripts module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

turboshell.reload

This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

turboshell  cmd-name  [args]







Manual

Scripts

TODO: flesh out.

Commands

You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

    def say_hello(args):
        pass
    
    ac.cmd(say_hello)

This registers the function using its name, so you can invoke it like this:

    $ turboshell say_hello

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

    ac.cmd(say_hello, name='my-hello-cmd')

The name is usually not so relevant as you typically create aliased for these command.

Aliases

You create aliases to shell commands like so:

    ac.alias('grep-py', 'grep -r --include=*.{py}')

To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

    ac.alias('hello', 'turboshell say_hello')
    ac.alias('hello-spanish', 'turboshell say_hello ES')

Just like normal aliases, you can preset some parameters in the alias if your function handles them:

    ac.alias('hello-spanish', 'turboshell say_hello ES')
    ac.alias('hello-spanish', 'turboshell say_hello FR')

You can also creating an alias without parameters at the same time as passing a command.

    ac.cmd(say_hello, 'hello')

Info

The turboshell.info command prints something like this:

      turboshell.info    | Shows info on commands
      turboshell.rebuild | Rebuilds and reloads the aliases in current shell
      turboshell.reload  | Reloads the aliases in current shell

You can add items in there by providing an extra string to ac.alias():

    ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

Or if declaring the alias directly in the call to ac.cmd():

    ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

    def cmd(self, function, alias=None, info=None, name=None):
        pass

You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

    ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

Finally, you may explicitly add info entries separately from aliases:

    ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

This is useful for aliases which have many permutations. 

Arguments

TODO: flesh out (and provide decorators)



How does it work?

Once you've installed it (see Installation below) you get the following command in your shell:

turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your scripts module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

turboshell.reload

This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

turboshell  cmd-name  [args]

This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
2. Load all the Python code in your scripts module
3. Find the function which you registered with the same name.
4. Call that function, passing the command line arguments as a list of strings.




This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
2. Load all the Python code in your scripts module
3. Find the function which you registered with the same name.
4. Call that function, passing the command line arguments as a list of strings.


my_projects = {
    'project1': 'path/to/project'
    # Add all of your git projects in here, or store as a json file.
}

for project, path in my_projects.items():
    
    # Show git status of project without leaving your directory
    alias = 'gitstatus.{}'.format(project)
    cmd = "cd '{}' && git status && cd -".format(path)
    ts.alias(alias, cmd)
    
    # Quickly cd to project directory
    alias = 'cd.{}'.format(project)
    cmd = "cd '{}'".format(path)
    ts.alias(alias, cmd)
```

There are endless possibilities to what you can do, and how much time you can save.

Manual

Scripts

TODO: flesh out.

Commands

You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

    def say_hello(args):
        pass
    
    ac.cmd(say_hello)

This registers the function using its name, so you can invoke it like this:

    $ turboshell say_hello

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

    ac.cmd(say_hello, name='my-hello-cmd')

The name is usually not so relevant as you typically create aliased for these command.

Aliases

You create aliases to shell commands like so:

    ac.alias('grep-py', 'grep -r --include=*.{py}')

To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

    ac.alias('hello', 'turboshell say_hello')
    ac.alias('hello-spanish', 'turboshell say_hello ES')

Just like normal aliases, you can preset some parameters in the alias if your function handles them:

    ac.alias('hello-spanish', 'turboshell say_hello ES')
    ac.alias('hello-spanish', 'turboshell say_hello FR')

You can also creating an alias without parameters at the same time as passing a command.

    ac.cmd(say_hello, 'hello')

Info

The turboshell.info command prints something like this:

      turboshell.info    | Shows info on commands
      turboshell.rebuild | Rebuilds and reloads the aliases in current shell
      turboshell.reload  | Reloads the aliases in current shell

You can add items in there by providing an extra string to ac.alias():

    ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

Or if declaring the alias directly in the call to ac.cmd():

    ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

    def cmd(self, function, alias=None, info=None, name=None):
        pass

You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

    ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

Finally, you may explicitly add info entries separately from aliases:

    ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

This is useful for aliases which have many permutations. 

Arguments

TODO: flesh out (and provide decorators)



How does it work?

Once you've installed it (see Installation below) you get the following command in your shell:

turboshell.info

This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

turboshell.rebuild

This command will:

1. Activate the virtual environment
2. Load all the Python code in your scripts module
3. Collect all the aliases
4. Write those to a file
5. Source from that file to bring the newly written aliase into the current shell session. 

During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

turboshell.reload

This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

turboshell  cmd-name  [args]

This command will:

1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)

2. Load all the Python code in your scripts module

3. Find the function which you registered with the same name.

4. Call that function, passing the command line arguments as a list of strings.Manual

   Scripts

   TODO: flesh out.

   Commands

   You create a command by defining a function and passing it to ac.cmd(). Note that the function must take a single parameter which will be a list of strings.

       def say_hello(args):
           pass
       
       ac.cmd(say_hello)

   This registers the function using its name, so you can invoke it like this:

       $ turboshell say_hello

   If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

       ac.cmd(say_hello, name='my-hello-cmd')

   The name is usually not so relevant as you typically create aliased for these command.

   Aliases

   You create aliases to shell commands like so:

       ac.alias('grep-py', 'grep -r --include=*.{py}')

   To create an alias for a command defined in turboshell, simply set the command to turboshell cmd-name:

       ac.alias('hello', 'turboshell say_hello')
       ac.alias('hello-spanish', 'turboshell say_hello ES')

   Just like normal aliases, you can preset some parameters in the alias if your function handles them:

       ac.alias('hello-spanish', 'turboshell say_hello ES')
       ac.alias('hello-spanish', 'turboshell say_hello FR')

   You can also creating an alias without parameters at the same time as passing a command.

       ac.cmd(say_hello, 'hello')

   Info

   The turboshell.info command prints something like this:

         turboshell.info    | Shows info on commands
         turboshell.rebuild | Rebuilds and reloads the aliases in current shell
         turboshell.reload  | Reloads the aliases in current shell

   You can add items in there by providing an extra string to ac.alias():

       ac.alias('hello', 'turboshell say_hello', 'Prints hello. Args: name.')

   Or if declaring the alias directly in the call to ac.cmd():

       ac.cmd(say_hello, 'hello', 'Prints hello. Args: name.')

   Note that for cmd() the info is only used if alias is specified. The signature of cmd is:

       def cmd(self, function, alias=None, info=None, name=None):
           pass

   You must provide arguments in the correct sequence, or specify keyword args as Python's rules:

       ac.cmd(say_hello, 'hello', name='my-hello-cmd', info='Prints hello. Args: name.')

   Finally, you may explicitly add info entries separately from aliases:

       ac.info('hello-[lang]', 'Prints hello in [lang]. Args: name.')

   This is useful for aliases which have many permutations. 

   Arguments

   TODO: flesh out (and provide decorators)

   

   How does it work?

   Once you've installed it (see Installation below) you get the following command in your shell:

   turboshell.info

   This prints out some info including the list of available commands. You can add to this from your Python code (see Manual below).

   turboshell.rebuild

   This command will:

   1. Activate the virtual environment
   2. Load all the Python code in your scripts module
   3. Collect all the aliases
   4. Write those to a file
   5. Source from that file to bring the newly written aliase into the current shell session. 

   During installation you'll be told to source from that file in your .bashrc file (or equivalent) which ensures these aliases are available in new shell sessions.

   turboshell.reload

   This is just an alias for source /path/to/generated/alias/file. Use this command if you called turboshell.rebuild in another shell session and want to reload the new aliases into the current session.

   turboshell  cmd-name  [args]

   This command will:

   1. Activate the virtual environment (in a new shell context, so doesn't affect your active shell)
   2. Load all the Python code in your scripts module
   3. Find the function which you registered with the same name.
   4. Call that function, passing the command line arguments as a list of strings.



Turboshell is a tool which lets you do two things:

#### 1. Write shell commands in Python

The following code:

```python
from turboshell import cmd

@cmd(args='name', alias='hello')
def say_hello(name):
    print('Hello {}!'.format(name))
```

Creates a shell command which accepts a single argument:

```bash
$ hello Ana
Hello Ana!
```

This may look a bit like [click](https://palletsprojects.com/p/click/) or [invoke](), but there's a big difference. With click or invoke you need to:

1. Activate the right virtual environment
2. Be in the same directory as your file (or type the path to it)
3. Type something ugly like `python hello.py --name Ana`

Turboshell however creates a normal shell command (alias) which will be available in every new shell session, and can be called from any directory. The virtual environment is also handled automatically.

The tools have different objectives:

* Click and invoke are tools for creating commands to be shared with others. If people want to make aliases for the commands, that's up to them.
* Turboshell is aimed at creating commands and aliases to existing commands, as quickly as possible, for your personal use.



* 
* is a tool for turbocharging your own shell to maximise your productivity. It assumes you are writing commands for your own use and therefore want aliases for them. You can of course share your commands (via pip, github etc...) and let others alias the commands how they like.

#### 2. Generate shell aliases using python

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

You create a command by defining a function and passing it to `ac.cmd()`. Note that the function must take a single parameter which will be a list of strings.

```python
def say_hello(args):
    pass

ac.cmd(say_hello)
```

This registers the function using its name, so you can invoke it like this:

```
$ turboshell say_hello
```

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

```python
ac.cmd(say_hello, name='my-hello-cmd')
```

The name is usually not so relevant as you typically create aliased for these command.

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









--------------









## Manual

### Scripts

TODO: flesh out.

### Commands

You create a command by defining a function and passing it to `ac.cmd()`. Note that the function must take a single parameter which will be a list of strings.

```python
def say_hello(args):
    pass

ac.cmd(say_hello)
```

This registers the function using its name, so you can invoke it like this:

```
$ turboshell say_hello
```

If you want a different name, perhaps to avoid clashes with a command in a different module, you can specify a name like this:

```python
ac.cmd(say_hello, name='my-hello-cmd')
```

The name is usually not so relevant as you typically create aliased for these command.

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

