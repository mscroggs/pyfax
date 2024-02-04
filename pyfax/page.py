"""Functions to create teletext pages."""

import os
from enum import Enum
from typing import Dict, Union

from ._config import config

BCHARS = {
    "      ": " ", "x     ": "!", " x    ": "\"", "xx    ": "#", "  x   ": "$",
    "x x   ": "%", " xx   ": "&", "xxx   ": "'", "   x  ": "(", "x  x  ": ")",
    " x x  ": "*", "xx x  ": "+", "  xx  ": ",", "x xx  ": "-", " xxx  ": ".",
    "xxxx  ": "/", "    x ": "0", "x   x ": "1", " x  x ": "2", "xx  x ": "3",
    "  x x ": "4", "x x x ": "5", " xx x ": "6", "xxx x ": "7", "   xx ": "8",
    "x  xx ": "9", " x xx ": ":", "xx xx ": ";",  "  xxx ": "<", "x xxx ": "=",
    " xxxx ": ">", "xxxxx ": "?", "     x": "`", "x    x": "a", " x   x": "b",
    "xx   x": "c", "  x  x": "d", "x x  x": "e", " xx  x": "f", "xxx  x": "g",
    "   x x": "h", "x  x x": "i", " x x x": "j", "xx x x": "k", "  xx x": "l",
    "x xx x": "m", " xxx x": "n", "xxxx x": "o", "    xx": "p", "x   xx": "q",
    " x  xx": "r", "xx  xx": "s", "  x xx": "t", "x x xx": "u", " xx xx": "v",
    "xxx xx": "w", "   xxx": "x", "x  xxx": "y", " x xxx": "z", "xx xxx": "{",
    "  xxxx": "|", "x xxxx": "}", " xxxxx": "~", "xxxxxx": "\x7f",
}


class Color(Enum):
    """Enum to store colors."""
    DEFAULT = 0
    WHITE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    CYAN = 5
    MAGENTA = 6
    YELLOW = 7
    BLACK = 8


COLCHARS = {
    Color.DEFAULT: "G",
    Color.WHITE: "G",
    Color.RED: "A",
    Color.GREEN: "B",
    Color.BLUE: "D",
    Color.CYAN: "F",
    Color.MAGENTA: "E",
    Color.YELLOW: "C",
}

BLOCKCOLCHARS = {
    Color.DEFAULT: "W",
    Color.WHITE: "W",
    Color.RED: "Q",
    Color.GREEN: "R",
    Color.BLUE: "T",
    Color.CYAN: "V",
    Color.MAGENTA: "U",
    Color.YELLOW: "S",
}


class Line:
    """A line of a teletext page."""

    def __init__(self):
        """Initialise the line."""
        self.chars = []

    def __str__(self) -> str:
        """Convert the line to a string."""
        if len(self.chars) > 40:
            print(f"line is too long ({len(self.chars)} characters, max 40):")
            print(''.join(self.chars))
        assert len(self.chars) <= 40
        return "".join(self.chars)

    def __len__(self) -> int:
        """Get the length of the line."""
        return len(self.chars)

    def start_double_size(self):
        """Start a double sized block of text."""
        self.chars.append("\x1bM")

    def end_double_size(self):
        """End a double sized block of text."""
        self.chars.append("\x1bL")

    def start_flashing(self):
        """Start a flashing block of text."""
        self.chars.append("\x1bH")

    def end_flashing(self):
        """End a flashing block of text."""
        self.chars.append("\x1bI")

    def start_fg(self, color: Color, block: bool = False):
        """Start a foreground color.

        Args:
            color: The color.
            block: Is this a blocked drawing?
        """
        if block:
            self.chars.append("\x1b" + BLOCKCOLCHARS[color])
        else:
            self.chars.append("\x1b" + COLCHARS[color])

    def add_text(self, text: str):
        """Add text to the line.

        Args:
            text: The text.
        """
        self.chars += [i for i in text]

    def add_block(self, block: str, color: Color, color_after: Color = Color.WHITE):
        """Add a blocked drawing to the line.

        Args:
            block: The blocked drawing. This should have three lines separated by
                newline characters. xs should be used for filled squares and .s
                for non-filled squares.
            color: The color.
            color_after: The color to use after the blocked drawing
        """
        block = block.replace(".", " ")
        blocks = block.strip("\n").split("\n")
        text = ""
        for char in zip(*[b[j::2] for b in blocks for j in range(2)]):
            text += BCHARS["".join(char)]
        self.start_fg(color, True)
        self.add_text(text)
        if color_after is not None:
            self.start_fg(color_after)

    def start_bg(self, color: Color):
        """Start a background color.

        Args:
            color: The color.
        """
        if color in [Color.BLACK, Color.DEFAULT]:
            self.chars.append("\x1b\\")
        else:
            self.start_fg(color)
            self.chars.append("\x1b]")


class Page:
    """A teletext page."""

    def __init__(self, page_number: int):
        """Initialise a page.

        Args:
            page_number: The page number.
        """
        assert 100 <= page_number < 900
        self.description = None
        self.page_number = page_number
        self.subpage = 1
        self.ps = 8010
        self.lines: Dict[int, Union[Line, None]] = {i: None for i in range(1, 26)}
        self.tagline = "EMFFAX: The world at your fingertips"

    def write(self, overwrite: bool = False):
        """Write the page to file in the build directory.

        Args:
            overwrite: Overwrite existing pages?
        """
        assert self.page_number != 888
        if not overwrite:
            if os.path.isfile(f"{config.build_dir}/P{self.page_number}.tti"):
                raise RuntimeError(f"Duplicate page: {self.page_number}")
        with open(f"{config.build_dir}/P{self.page_number}.tti", "w") as f:
            f.write(self.to_tti())

    def write_direct(self, overwrite: bool = False):
        """Write the page directly to the output directory.

        Args:
            overwrite: Overwrite existing pages?
        """
        if not overwrite:
            if os.path.isfile(f"{config.output_dir}/P{self.page_number}.tti"):
                raise RuntimeError(f"Duplicate page: {self.page_number}")
        with open(f"{config.output_dir}/P{self.page_number}.tti", "w") as f:
            f.write(self.to_tti())

    def to_tti(self) -> str:
        """Convert the page to a tti string."""
        if self.tagline is not None:
            tagline = " " * ((35 - len(self.tagline)) // 2) + self.tagline
            tagline += " " * (36 - len(tagline))
            line = Line()
            line.start_bg(Color.BLUE)
            line.start_fg(Color.YELLOW)
            line.add_text(tagline)
            line.start_bg(Color.BLACK)
            self.lines[22] = line

        assert self.page_number is not None
        padded_subpage = f"000{self.subpage}"[-2:]
        out = ""
        out += f"DE,{self.description}\n"
        out += f"PS,{self.ps}\n"
        out += f"PN,{self.page_number}{padded_subpage}\n"
        out += f"SC,00{padded_subpage}\n"
        for i, j in self.lines.items():
            if j is not None:
                out += f"OL,{i},{j}\n"

        return out

    def set_line(self, number: int, line: Line):
        """Set a line of the page.

        Args:
            number: The line number.
            line: The line.
        """
        assert number in self.lines
        # Save space for tagline
        assert number not in [21, 22, 23]
        self.lines[number] = line

    def set_tagline(self, tagline: str):
        """Set the tagline of the page.

        Args:
            tagline: The tagline.
        """
        assert tagline is None or len(tagline) <= 36
        self.tagline = tagline

    def add_wrapped_text(
        self, number: int, text: str, double: bool = False,
        color: Color = Color.DEFAULT
    ) -> int:
        """Add wrapped text to the page.

        Args:
            number: The line number to start the text.
            text: The text.
            double: Should the text be double sized?
            color: The text color.

        Returns:
            The line number after the text finishes.
        """
        words = text.split()
        words = [i if len(i) < 35 else i[:5] + "..." + i[-5:] for i in words]

        if len(words) == 0:
            return number

        line = Line()
        if double:
            line.start_double_size()
            if color != Color.DEFAULT:
                line.start_fg(color)
        else:
            line.start_fg(color)
        while True:
            if len(line) + len(words[0]) + 1 >= 40:
                self.set_line(number, line)
                line = Line()
                if double:
                    line.start_double_size()
                    if color != Color.DEFAULT:
                        line.start_fg(color)
                    number += 2
                else:
                    line.start_fg(color)
                    number += 1
                if number > 20:
                    return number
            if len(line) == 1:
                line.add_text(words[0])
            else:
                line.add_text(" " + words[0])
            words = words[1:]
            if len(words) == 0:
                self.set_line(number, line)
                if double:
                    return number + 2
                else:
                    return number + 1

    def add_block(
        self, number: int, block: str, color: Color,
        bg: Union[Color, None] = None, indent: int = 0, color_after: Color = Color.WHITE
    ) -> int:
        """Add a block drawing to the page.

        Args:
            number: The line number to start the block drawing.
            block: The blocked drawing. This should have a number of lines that
                is a mutliple of three separated by newline characters. xs should
                be used for filled squares and .s for non-filled squares.
            color: The text color.
            bg: The background color.
            index: The number of characters to indent the drawing.
            color_after: The color to use afer the block drawing.

        Returns:
            The line number after the block drawing finishes.
        """
        blocks = block.strip("\n").split("\n")
        assert len(blocks) % 3 == 0
        for i in range(0, len(blocks), 3):
            line = Line()
            if bg is not None:
                line.start_bg(bg)
            if indent > 0:
                line.add_text(" " * indent)
            line.add_block("\n".join(blocks[i:i+3]), color, color_after)
            self.set_line(number, line)
            number += 1
        return number
