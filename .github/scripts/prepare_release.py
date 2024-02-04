"""Script to prepare files for uploading to PyPI."""

import argparse
import os

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")

parser = argparse.ArgumentParser(description="Build defelement.com")
parser.add_argument('--version', metavar='version',
                    default="main", help="pyfax version.")
version = parser.parse_args().version
if version != "main":
    version = "v" + version

with open(os.path.join(root_dir, "README.md")) as f:
    parts = f.read().split("](")

content = parts[0]

for p in parts[1:]:
    content += "]("
    if not p.startswith("http"):
        content += f"https://raw.githubusercontent.com/mscroggs/pyfax/{version}/"
    content += p

with open(os.path.join(root_dir, "README.md"), "w") as f:
    f.write(content)
