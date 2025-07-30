"""
File containing data parsers for ClippingsService class.

Constants:
    BOOK_WITH_PARENTHESES_REGEX (str) - Regex to handle book title Clipping line, like "Book title (Book author)".
    BOOK_WITH_DASH_REGEX (str) - Regex to handle book title Clipping line, like "Book title - Book author".
    METADATA_WITH_PAGE_REGEX (str) - Regex to handle Clipping metadata line with page as first mentioned param, like
    "- Your Highlight on page 3 | location 41-41 | Added on Monday, 6 February 2023 06:32:11"
    METADATA_WITHOUT_PAGE_REGEX (str) - Regex to handle Clipping metadata line without page as first mentioned
    param, like "- Your Bookmark at location 579 | Added on Tuesday, 27 September 2022 15:45:30".
"""

import re
from datetime import datetime

BOOK_WITH_PARENTHESES_REGEX: str = r"^(.*) \((.*)\)$"
BOOK_WITH_DASH_REGEX: str = r"^(.*) - (.*)$"
METADATA_WITH_PAGE_REGEX: str = (
    r"^- [yY]our (\w+) [oO]n [pP]age (\d+|\d+-\d+) \| ([lL]ocation (\d+|\d+-\d+) \| )?[aA]dded on (\w+), (.*)$"
)
METADATA_WITHOUT_PAGE_REGEX: str = r"^- [yY]our (\w+) [aA]t [lL]ocation (\d+|\d+-\d+) \| [aA]dded on (\w+), (.*)$"


def parse_book_line(line: str) -> dict:
    """
    Parses book line of Clipping with REGEX to extinguish Book title and author.

    Args:
        line (str): File line.

    Returns:
        dict: Dictionary containing Book namedtuple in "book" key or empty one.
    """
    line = line.replace("\xa0", " ").replace("\ufeff", "")
    if match := re.match(BOOK_WITH_PARENTHESES_REGEX, line):
        book_title, author = match.groups()
    elif match := re.match(BOOK_WITH_DASH_REGEX, line):
        book_title, author = match.groups()
    else:
        return {}
    return {"book": {"title": book_title.strip(), "author": author.strip()}}


def parse_metadata_line(line: str) -> dict:
    """
    Parses metadata line of Clipping with REGEX to extinguish Clipping metadata - Clipping type, page number,
    location and creation datetime.

    Args:
        line (str): File line.

    Returns:
        dict: Dictionary containing Clipping metadata or empty one.
    """
    data = {}
    if match := re.match(METADATA_WITH_PAGE_REGEX, line):
        groups = match.groups()
        data["clipping_type"] = groups[0]
        data["page_number"] = groups[1]
        data["location"] = groups[3]
        data["created_at"] = datetime.strptime(groups[5], "%d %B %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    elif match := re.match(METADATA_WITHOUT_PAGE_REGEX, line):
        groups = match.groups()
        data["clipping_type"] = groups[0]
        data["page_number"] = None
        data["location"] = groups[1]
        data["created_at"] = datetime.strptime(groups[3], "%d %B %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    return data


def parse_content_line(line: str) -> dict:
    """
    Parses content line of Clipping to get rid of unnecessary signs:
    * \xa0 - replaces non-breaking space character with regular space.

    Args:
        line (str): File line.

    Returns:
        dict: Dictionary containing cleared "content" key data.
    """
    return {"content": line.replace("\xa0", " ").strip()}
