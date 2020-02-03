from turboshell import ac

ac.alias('grep-py', 'grep -r --include=*.py')
ac.alias('grep-js', 'grep -r --include=*.js')


langs = {'FR': 'Bonjour', 'ES': 'Hola', 'EN': 'Hello'}


def say_hello(args):
    lang = args[0]
    name = args[1]
    print('{} {}!'.format(langs[lang], name))

# Regitser function as a turboshell command
ac.cmd(say_hello)

# Create alises:
ac.alias('hello', 'turboshell say_hello EN')
ac.alias('hello-spanish', 'turboshell say_hello ES')
ac.alias('hello-french', 'turboshell say_hello FR')
