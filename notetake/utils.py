import subprocess as sub
from notetake import EDITOR


def fzf(args) -> str:
    if len(args) == 0:
        return
    input_str = ''
    for arg in args:
        input_str += arg + '\n'
    fzf = sub.run('fzf', input=input_str, encoding='utf-8', stdout=sub.PIPE)
    print(fzf.stdout.strip())
    return fzf.stdout.strip()

def editor(filepath) -> None:
    if filepath is None:
        return
    args = [EDITOR]
    args += [filepath]
    sub.run(args, encoding='utf-8')

def update_config() -> None:
    ...
