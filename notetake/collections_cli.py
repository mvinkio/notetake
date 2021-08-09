from notetake import CONFIG
from pathlib import Path

from notetake.utils import fzf
from notetake.collections import Collections

import typer


app = typer.Typer()


@app.command()
def new(name: str = typer.Argument(None)):
    print("making new collection")
    if name is None:
        name = input("give a name for the new collection: ")

    with Collections(CONFIG) as c:
        c.new(name)


@app.command()
def edit():
    with Collections(CONFIG) as c:
        collections_with_modules = [path.as_posix()
                for path
                in Path(CONFIG['note_paths']['collections']).glob('*/*/parts')]
        c.edit(fzf(
            collections_with_modules
            ))

@app.command()
def add():
    collections = [path.as_posix()
                   for path
                   in Path(CONFIG['note_paths']['collections']).glob('*')]

    if len(collections) == 0:
        typer.echo("there were no collections!")
        return

    with Collections(CONFIG) as c:
        collection = fzf(collections)
        name = input("what is the name of the new module?: ")
        while not c.add(Path(collection), name):
            name = input("what is the name of the new module?: ")


if __name__ == '__main__':
    app()
