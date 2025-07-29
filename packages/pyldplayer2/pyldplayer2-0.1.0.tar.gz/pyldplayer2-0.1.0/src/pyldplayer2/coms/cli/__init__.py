import click

from pyldplayer2.coms.instanceQuery import Query
from .layout import get_affected_string

importExceptions = None
try:
    from .consoleCmds import cmd, console
except Exception as e:
    click.echo("Failed to initialize console commands", err=True)
    importExceptions = e


@click.group(invoke_without_command=True)
@click.option("-d", "--debug", is_flag=True, help="enable debug mode")
@click.option("-q", "--query", help="set console scope")
@click.option("-I", "--interval", help="set batch interval", type=int)
@click.pass_context
def cli(ctx: click.Context, debug: bool, query: str, interval: int):
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug

    if importExceptions and debug:
        raise importExceptions
    assert console is not None, "Failed to initialize console"

    if interval:
        console.interval = interval

    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())

    if query:
        results = Query().query(query)
        console.setScope(results)
        ctx.obj["scope"] = results
    else:
        results = Query().query(console.scope)
    click.echo(f"scope: {get_affected_string(results)}")


cli.add_command(cmd)

if __name__ == "__main__":
    cli()
