import pyfax
from pyfax import Page, Line, Color
import os

lipsum = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
          "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis "
          "nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
          "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu "
          "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in "
          "culpa qui officia deserunt mollit anim id est laborum.")


def test_text():
    text = "Hello there."
    p1 = Page(100)
    line = Line()
    line.start_fg(Color.DEFAULT)
    line.add_text(text)
    p1.set_line(2, line)

    p2 = Page(100)
    p2.add_wrapped_text(2, text)

    for i, j in p1.lines.items():
        assert str(j) == str(p2.lines[i])

    assert p1.to_tti() == p2.to_tti()


def test_block():
    block = (
        "xx.x.xx...x.\n"
        "x.xx...x..x.\n"
        "xx.xx...x.x.\n"
    )
    p1 = Page(100)
    line = Line()
    line.add_block(block, Color.RED)
    p1.set_line(2, line)

    p2 = Page(100)
    p2.add_block(2, block, Color.RED)

    for i, j in p1.lines.items():
        assert str(j) == str(p2.lines[i])

    assert p1.to_tti() == p2.to_tti()


def text_wrapped_text():
    p = Page(100)
    p.add_wrapped_text(2, lipsum)

    p = Page(101)
    p.add_wrapped_text(2, lipsum, double=True)


def test_tagline():
    p = Page(100)
    p.set_tagline("TAGLINE")


def test_test_page():
    pyfax.config.build_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "_pages")

    os.system(f"rm -rf {pyfax.config.build_dir}")
    assert os.system(f"mkdir {pyfax.config.build_dir}") == 0

    pyfax.pages.make_test_page()
