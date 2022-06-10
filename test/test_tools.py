import os
import json
from pyfax.tools import url_helpers


def test_json_url_helper():
    data = url_helpers.load_json(
        "https://raw.githubusercontent.com/mscroggs/pyfax/main/test/data/json.json")

    with open(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.path.join("data", "json.json"))
    ) as f:
        data2 = json.load(f)

    assert data == data2
