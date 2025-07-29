def cli_compat():
    """
    reldplay compatiblity layer to allow past scripts to work
    """
    import sys

    sys.argv[0] = sys.argv[0].replace("reldplay", "ldplay")

    counter = 1
    while counter < len(sys.argv):
        if sys.argv[counter].startswith("-"):
            counter += 2
        else:
            break

    sys.argv.insert(counter, "cmd")

    from pyldplayer2.coms.cli import cli

    cli()


if __name__ == "__main__":
    cli_compat()
