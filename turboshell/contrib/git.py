from turboshell import ts

ts.func('gcm', 'git commit -m "$*"')
ts.func('gacm', 'git add -A && git commit -m "$*"')

ts.alias('gs', 'git status')
ts.alias('gl', 'git log --stat')
ts.alias('gag', 'git update-index --again')


for cmd in ['show', 'status', 'log', 'checkout', 'commit', 'pull', 'push']:
    ts.alias(f'git.{cmd}', f'git {cmd}')
