import click
from pyldplayer2.coms.batchConsole import BatchConsole
from pyldplayer2.utils.discover import discover
from .layout import CustomGroup

try:
    discover()
    console = BatchConsole()
except Exception:
    console = None


@click.group(cls=CustomGroup)
def cmd():
    pass


@cmd.command("list2")
@click.pass_context
def list2(ctx: click.Context):
    click.echo("command: list2")
    from tabulate import tabulate
    headers = ["name", "id", "twh", "bwh", "pid"]
    data = []
    scope = ctx.obj.get("scope", console.list2())
    for meta in scope:
        if meta["id"] == 0:
            continue
        data.append([
            meta["name"],
            meta["id"],
            meta["top_window_handle"],
            meta["bind_window_handle"],
            meta["pid"]
        ])
    click.echo(tabulate(data, headers=headers, tablefmt="plain"))
#


@cmd.command()
def rock():
    click.echo("command: rock")
    console.rock()


@cmd.command()
def quitall():
    click.echo("command: quitall")
    console.quitall()


@cmd.command()
def zoomOut():
    click.echo("command: zoomOut")
    console.zoomOut()


@cmd.command()
def zoomIn():
    click.echo("command: zoomIn")
    console.zoomIn()


@cmd.command()
def sortWnd():
    click.echo("command: sortWnd")
    console.sortWnd()


#
@cmd.command()
def quit():
    click.echo("command: quit")
    console.quit()


@cmd.command()
def launch():
    click.echo("command: launch")
    console.launch()


@cmd.command()
def reboot():
    click.echo("command: reboot")
    console.reboot()


# SECTION -
@cmd.command()
@click.option("--from", "-f", "from_", help="copy from this instance")
def copy(from_: str):
    console.copy(_from=from_)


@cmd.command()
@click.option("--title", "-t", help="new title")
def rename(title: str):
    console.rename(title=title)


@cmd.command()
@click.option("--package", "-p", required=True, help="package name")
@click.option("--file", "-f", required=True, help="apk file path")
def installapp(package: str, file: str):
    console.installapp(packagename=package, filename=file)


@cmd.command()
@click.option("--package", "-p", required=True, help="package name")
def uninstallapp(package: str):
    console.uninstallapp(packagename=package)


@cmd.command()
@click.option("--package", "-p", required=True, help="package name")
def runapp(package: str):
    console.runapp(packagename=package)


@cmd.command()
@click.option("--package", "-p", required=True, help="package name")
def killapp(package: str):
    console.killapp(packagename=package)


@cmd.command()
@click.option("--lli", "-l", required=True, help="LLI parameter")
@click.pass_context
def locate(lli: str):
    console.locate(LLI=lli)


@cmd.command()
@click.option("--command", "-c", required=True, help="ADB command to execute")
def adb(command: str):
    console.adb(command=command)


@cmd.command()
@click.option("--key", "-k", required=True, help="property key")
@click.option("--value", "-v", required=True, help="property value")
@click.pass_context
def setprop(key: str, value: str):
    console.setprop(key=key, value=value)


@cmd.command()
@click.option("--rate", "-r", required=True, type=int, help="CPU rate")
def downcpu(rate: int):
    console.downcpu(rate=rate)


@cmd.command()
@click.option("--file", "-f", required=True, help="backup file path")
@click.pass_context
def backup(file: str):
    console.backup(file=file)


@cmd.command()
@click.option("--file", "-f", required=True, help="restore file path")
def restore(file: str):
    console.restore(file=file)


@cmd.command()
@click.option("--key", "-k", required=True, help="action key")
@click.option("--value", "-v", required=True, help="action value")
def action(key: str, value: str):
    console.action(key=key, value=value)


@cmd.command()
@click.option("--file", "-f", required=True, help="scan file path")
def scan(file: str):
    console.scan(file=file)


@cmd.command()
@click.option("--remote", "-r", required=True, help="remote path")
@click.option("--local", "-l", required=True, help="local path")
def pull(remote: str, local: str):
    console.pull(remote=remote, local=local)


@cmd.command()
@click.option("--remote", "-r", required=True, help="remote path")
@click.option("--local", "-l", required=True, help="local path")
def push(remote: str, local: str):
    console.push(remote=remote, local=local)


@cmd.command()
@click.option("--package", "-p", required=True, help="package name")
@click.option("--file", "-f", required=True, help="backup file path")
def backupapp(package: str, file: str):
    console.backupapp(packagename=package, file=file)


@cmd.command()
@click.option("--package", "-p", required=True, help="package name")
@click.option("--file", "-f", required=True, help="restore file path")
def restoreapp(package: str, file: str):
    console.restoreapp(packagename=package, file=file)


@cmd.command()
@click.option("--package", "-p", required=True, help="package name")
def launchex(package: str):
    console.launchex(packagename=package)


@cmd.command()
@click.option("--content", "-c", required=True, help="record content")
def operaterecord(content: str):
    console.operaterecord(content=content)
