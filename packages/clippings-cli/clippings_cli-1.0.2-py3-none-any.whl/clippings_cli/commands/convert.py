import os
import sys

import click

from clippings_cli.clippings_service.service import ClippingsService


def get_full_input_path(path: str | None) -> str | None:
    """
    Function to evaluate full path to Clippings file based on input path.

    Args:
        path (str | None): Path to Clippings file or None.

    Returns:
        str | None: Full path to Clippings file or None in case of errors.
    """
    if not path:
        path = os.path.normpath(os.path.join(os.getcwd(), "My Clippings.txt"))
    elif os.path.isabs(os.path.normpath(path)):
        pass
    else:
        path = os.path.normpath(os.path.join(os.getcwd(), path))
    if not os.path.exists(path):
        click.echo(click.style(f"Path [{path}] does not exist.", fg="red", underline=True), err=True)
        return None
    elif not os.path.isfile(path):
        click.echo(click.style(f"Path [{path}] is not a file.", fg="red", underline=True), err=True)
        return None
    elif not path.endswith(".txt"):
        click.echo(click.style(f"Path [{path}] is not a .txt file.", fg="red", underline=True), err=True)
        return None
    return path


def get_full_output_path(path: str | None, format: str | None) -> str | None:
    """
    Function to evaluate full path to Clippings file based on input path.

    Args:
        path (str | None): Path to Clippings file or None.

    Returns:
        str | None: Full path to Clippings file or None in case of errors.
    """
    match format:
        case "json":
            extension = "json"
        case "excel":
            extension = "xlsx"
        case _:
            return None
    if not path:
        path = os.path.normpath(os.path.join(os.getcwd(), f"Output.{extension}"))
    elif os.path.isabs(os.path.normpath(path)):
        pass
    else:
        path = os.path.normpath(os.path.join(os.getcwd(), path))
    return path


@click.command()
@click.option("-i", "--input_path", default=None, help="Path to Clippings file (full or relative).")
@click.option("-o", "--output_path", default=None, help="Path to output file (full or relative).")
@click.option(
    "-f",
    "--format",
    required=True,
    type=click.Choice(["json", "excel"], case_sensitive=False),
    help="Output format. [json|excel]",
)
def convert(input_path: str | None, output_path: str | None, format: str):
    """
    Convert Clippings file to one of supported formats. [json|excel]

    Args:

        input_path (str | None): Full or relative path to Clippings file. Searches for "My Clipping.txt" file in current
        directory by default.

        output_path (str | None): Full or relative path to output file. Creates output file in current
        directory by default.

        format (str): Demanded format of output. [json|excel]
    """

    full_input_path = get_full_input_path(input_path)
    full_output_path = get_full_output_path(output_path, format)

    if full_input_path is None or full_output_path is None:
        sys.exit(1)

    clippings_service = ClippingsService(input_path=full_input_path, output_path=full_output_path)
    click.echo(
        click.style(
            f"Output file generation started: \n* Format [{format}]\n"
            f"* Input path [{full_input_path}]\n* Output path [{full_output_path}]",
            fg="yellow",
            underline=True,
        ),
        err=False,
    )
    result = clippings_service.generate_output(format=format)

    if "error" in result:
        click.echo(
            click.style(
                f"Output file in [{format}] format generation finished with error [{result['error']}].",
                fg="red",
                underline=True,
            ),
            err=True,
        )
        sys.exit(1)
    else:
        click.echo(
            click.style(
                "Output file generation finished successfully.",
                fg="green",
                underline=True,
            ),
            err=False,
        )
        sys.exit(0)
