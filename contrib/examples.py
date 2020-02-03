from turboshell import ac

ac.alias('grep-py', 'grep -r --include=*.py')
ac.alias('grep-js', 'grep -r --include=*.js')


langs = {'FR': 'Bonjour', 'ES': 'Hola', 'EN': 'Hello'}


def say_hello(args):
    lang, name = args
    print('{} {}!'.format(langs[lang], name))

# Register function as a turboshell command
ac.cmd(say_hello)

# Create aliases:
ac.alias('hello', 'turboshell say_hello EN')
ac.alias('hello-spanish', 'turboshell say_hello ES')
ac.alias('hello-french', 'turboshell say_hello FR')
