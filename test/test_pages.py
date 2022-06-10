from pyfax import Page, Line


def test_text():
    p1 = Page(100)
    line = Line()
    line.add_text("Hello.")
    p1.set_line(2, line)

    p2 = Page(101)
    p2.add_wrapped_text(2, "Hello.")

    assert p1.lines == p2.lines
