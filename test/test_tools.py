import os
import json
from pyfax.tools import url_helpers
import pytest


def test_json_url_helper():
    data = url_helpers.load_json(
        "https://raw.githubusercontent.com/mscroggs/pyfax/main/test/data/json.json")

    try:
        with open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.path.join("data", "json.json"))
        ) as f:
            data2 = json.load(f)
    except FileNotFoundError:
        pytest.skip()

    assert data == data2


def test_csv_url_helper():
    data = url_helpers.load_csv(
        "https://raw.githubusercontent.com/mscroggs/pyfax/main/test/data/csv.csv")

    try:
        with open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.path.join("data", "csv.csv"))
        ) as f:
            data2 = [line.split(",") for line in f]
    except FileNotFoundError:
        pytest.skip()

    assert data == data2
