import typer

from mm_okx.cli.commands import account_commands, public_commands

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False, add_completion=False)


app.add_typer(public_commands.app, name="public")
app.add_typer(public_commands.app, name="p", hidden=True)


app.add_typer(account_commands.app, name="account")
app.add_typer(account_commands.app, name="a", hidden=True)
