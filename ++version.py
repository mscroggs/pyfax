"""
This script increases the version number of pyfax in all the relevant
locations. Once this has been run and the code pushed, emffaxbot will
automatically create a new version tag on GitHub.
"""

import json
from datetime import datetime

# Check that CHANGELOG_SINCE_LAST_VERSION.md is not empty
with open("CHANGELOG_SINCE_LAST_VERSION.md") as f:
    changes = f.read().strip()
if changes == "":
    raise RuntimeError("CHANGELOG_SINCE_LAST_VERSION.md should not be empty")

# Calculate new version number
with open("VERSION") as f:
    version = tuple(int(i) for i in f.read().split("."))

now = datetime.now()
if now.year == version[0] and now.month == version[1]:
    new_version = (now.year, now.month, version[2] + 1)
else:
    new_version = (now.year, now.month, 1)

new_version_str = ".".join([f"{i}" for i in new_version])

# VERSION file
with open("VERSION", "w") as f:
    f.write(new_version_str)

# codemeta.json
with open("codemeta.json") as f:
    data = json.load(f)
data["version"] = new_version_str
data["dateModified"] = now.strftime("%Y-%m-%d")
with open("codemeta.json", "w") as f:
    json.dump(data, f)

# setup.py
new_setup = ""
with open("setup.py") as f:
    for line in f:
        if 'version="' in line:
            a, b = line.split('version="')
            b = b.split('"', 1)[1]
            new_setup += f'{a}version="{new_version_str}"{b}'
        else:
            new_setup += line
with open("setup.py", "w") as f:
    f.write(new_setup)

# pyfax/version.py
with open("pyfax/version.py", "w") as f:
    f.write(f'"""Version number."""\n\nversion = "{new_version_str}"\n')

# .github/workflows/test-packages.yml
new_test = ""
url = "https://pypi.io/packages/source/s/pyfax/pyfax-"
with open(".github/workflows/test-packages.yml") as f:
    for line in f:
        if "ref:" in line:
            new_test += line.split("ref:")[0]
            new_test += f"ref: v{new_version_str}\n"
        elif url in line:
            new_test += line.split(url)[0]
            new_test += f"{url}{new_version_str}.tar.gz\n"
        elif "cd pyfax-" in line:
            new_test += line.split("cd pyfax-")[0]
            new_test += f"cd pyfax-{new_version_str}\n"
        else:
            new_test += line
with open(".github/workflows/test-packages.yml", "w") as f:
    f.write(new_test)

print(f"Updated version to {new_version_str}")
