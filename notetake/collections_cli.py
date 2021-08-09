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
        collection = fzf(c.get_collections())
        module = fzf(c.get_collections()[collection].get_modules())
        c.edit(collection, module)

@app.command()
def add():
    with Collections(CONFIG) as c:
        collections = c.get_collections()

        if len(collections.keys()) == 0:
            typer.echo("there were no collections!")
            return

        collection = fzf(collections.keys())
        name = input("what is the name of the new module?: ")
        while not c.add(collection, name):
            name = input("what is the name of the new module?: ")


if __name__ == '__main__':
    app()
