import subprocess as sub


def fzf(*args) -> str:
    input_str = ''
    for arg in args:
        input_str += arg + '\n'
    fzf = sub.run('fzf', input=input_str, encoding='utf-8', stdout=sub.PIPE)
    print(fzf.stdout.strip())
    return fzf.stdout.strip()

def editor() -> None:
    ...
