import typer
import notetake.collections_cli as collections

app = typer.Typer()
app.add_typer(collections.app, name="collections")


if __name__ == '__main__':
    app()
