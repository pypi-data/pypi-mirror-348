"""
File containing ClippingsService class that manages Clippings import from input file and content
conversion to one of supported formats.
"""

import click

from clippings_cli.clippings_service.format_handlers.excel_handlers import generate_excel
from clippings_cli.clippings_service.format_handlers.json_handlers import generate_json
from clippings_cli.clippings_service.parsers import parse_book_line, parse_content_line, parse_metadata_line
from clippings_cli.clippings_service.validators import validate_fields


class ClippingsService:
    """
    Class for retrieving Clippings from input Clippings file.

    Args:
        input_path (str): Full path to input Clippings file.
        output_path (str): Full path to output file.

    Attributes:
        clippings (list[dict]): List of collected Clippings.
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path: str = input_path
        self.output_path: str = output_path

    def _parse_clippings(self) -> list[dict]:
        """
        Parses Clippings source file and stores them in list of Clipping namedtuple objects.

        Example clipping:
        [Line 0] Django for APIs (William S. Vincent)
        [Line 1] - Your Highlight on page 9 | location 69-70 | Added on Sunday, 17 July 2022 18:00:00
        [Line 2]
        [Line 3] Clipping content.
        [Line 4] ==========

        Returns:
            list[Clipping]: List of Clipping namedtuples.
        """

        clippings = []
        with open(self.input_path, "r", encoding="utf8") as file:
            line_number = 0
            while line := file.readline():
                if line_number == 0:
                    clipping = {**parse_book_line(line)}
                elif line_number == 1:
                    clipping = {**clipping, **parse_metadata_line(line)}
                elif line_number == 2:
                    pass
                elif line_number == 3:
                    clipping = {**clipping, **parse_content_line(line)}
                elif line_number == 4:
                    line_number = -1
                    clipping["errors"] = validate_fields(clipping)
                    clippings.append(clipping)
                    clipping = {}
                line_number += 1
        return clippings

    def generate_output(self, format: str) -> dict:
        """
        In provided output_path creates file of given format containing data collected from Clippings input file.

        Args:
            format (str): Format of output file.

        Returns:
            dict: Dictionary containing data about potential errors.
        """
        clippings = self._parse_clippings()
        click.echo(click.style("Clippings file content loaded.", fg="green", underline=True), err=False)
        match format:
            case "json":
                return generate_json(clippings=clippings, output_path=self.output_path)
            case "excel":
                return generate_excel(clippings=clippings, output_path=self.output_path)
            case _:
                click.echo(click.style(f"Format [{format}] not supported.", fg="red", underline=True), err=True)
                return {"error": "Format not supported."}
