from pyfax import Page, Line, Color


def test_text():
    p1 = Page(100)
    line = Line()
    line.start_fg(Color.DEFAULT)
    line.add_text("Hello.")
    p1.set_line(2, line)

    p2 = Page(100)
    p2.add_wrapped_text(2, "Hello.")

    for i, j in p1.lines.items():
        assert str(j) == str(p2.lines[i])

    assert p1.to_tti() == p2.to_tti()
