import pyfax
import os


def test_test_page():
    pyfax.config.build_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "_pages")

    os.system(f"mkdir {pyfax.config.build_dir}")

    p = pyfax.Page(899)

    line = pyfax.Line()
    line.start_double_size()
    line.add_text("Test page")
    p.set_line(2, line)

    line = pyfax.Line()
    line.add_text("Foreground colours:")
    p.set_line(5, line)

    line = pyfax.Line()
    line.add_text(" " * 2)
    line.start_fg(pyfax.Color.RED)
    line.add_text("red")
    line.start_fg(pyfax.Color.GREEN)
    line.add_text("green")
    line.start_fg(pyfax.Color.BLUE)
    line.add_text("blue")
    line.start_fg(pyfax.Color.CYAN)
    line.add_text("cyan")
    line.start_fg(pyfax.Color.MAGENTA)
    line.add_text("magenta")
    p.set_line(6, line)

    line = pyfax.Line()
    line.add_text(" " * 2)
    line.start_fg(pyfax.Color.YELLOW)
    line.add_text("yellow")
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("white")
    line.start_fg(pyfax.Color.DEFAULT)
    line.add_text("default")
    p.set_line(7, line)

    line = pyfax.Line()
    line.add_text("Background colours:")
    p.set_line(9, line)

    line = pyfax.Line()
    line.add_text(" " * 2)
    line.start_bg(pyfax.Color.RED)
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("red")
    line.start_bg(pyfax.Color.DEFAULT)
    line.start_bg(pyfax.Color.GREEN)
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("green")
    line.start_bg(pyfax.Color.DEFAULT)
    line.start_bg(pyfax.Color.BLUE)
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("blue")
    line.start_bg(pyfax.Color.DEFAULT)
    line.start_bg(pyfax.Color.CYAN)
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("cyan")
    p.set_line(10, line)

    line = pyfax.Line()
    line.add_text(" " * 2)
    line.start_bg(pyfax.Color.MAGENTA)
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("magenta")
    line.start_bg(pyfax.Color.DEFAULT)
    line.start_bg(pyfax.Color.YELLOW)
    line.start_fg(pyfax.Color.BLUE)
    line.add_text("yellow")
    line.start_bg(pyfax.Color.DEFAULT)
    line.start_bg(pyfax.Color.WHITE)
    line.start_fg(pyfax.Color.BLUE)
    line.add_text("white")
    line.start_bg(pyfax.Color.DEFAULT)
    line.start_bg(pyfax.Color.BLACK)
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("black")
    p.set_line(11, line)

    line = pyfax.Line()
    line.add_text(" " * 2)
    line.start_bg(pyfax.Color.DEFAULT)
    line.start_fg(pyfax.Color.WHITE)
    line.add_text("default")
    p.set_line(12, line)

    line = pyfax.Line()
    line.add_text("Blocks:")
    p.set_line(14, line)

    line = pyfax.Line()
    for c in [pyfax.Color.WHITE, pyfax.Color.RED, pyfax.Color.GREEN, pyfax.Color.BLUE,
              pyfax.Color.CYAN, pyfax.Color.MAGENTA, pyfax.Color.YELLOW]:
        line.add_block(".xxx.xxx\n.x.x.x.x\nxx.xxx.x", c, None)
    p.set_line(15, line)

    p.write()

