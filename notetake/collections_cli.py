from notetake import CONFIG

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
def edit(col, module, part):
    with Collections(CONFIG) as c:
        typer.echo("editing collections")


@app.command()
def build():
    ...


if __name__ == '__main__':
    app()
