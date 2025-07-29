import click
import typing


def get_3_affected(res: typing.List[dict]):
    for item in res:
        yield item["name"] + "(" + str(item["id"]) + ")"


def get_affected_string(res: typing.List[dict]):
    string: str = ""
    for item in get_3_affected(res):
        if len(string) > 25:
            string += ", ..."
            break
        string += item + ", "
    return string


class CustomGroup(click.Group):
    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None or cmd.hidden:
                continue
            commands.append((subcommand, cmd))

        # Format commands in rows of 3
        if commands:
            rows = []
            current_row = []

            # Find the maximum length for padding
            max_len = max(len(cmd) for cmd, _ in commands)

            for i, (subcommand, cmd) in enumerate(commands):
                # Pad each command with spaces to ensure consistent width
                padded_command = subcommand.ljust(max_len)
                current_row.append(padded_command)
                if len(current_row) == 3:  # Split every 3 commands
                    rows.append(current_row)
                    current_row = []

            if current_row:  # Add any remaining commands
                while len(current_row) < 3:  # Pad with empty strings
                    current_row.append(" " * max_len)
                rows.append(current_row)

            with formatter.section("Commands"):
                for row in rows:
                    formatter.write("  " + "\t\t".join(row))
                    formatter.write("\n")
