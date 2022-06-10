name: 🧪

on:
  push:
    branches:
      - "**"
  pull_request:
    branches:
      - main

jobs:
  build-pages:
    name: Install and test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.7", "3.8", "3.9", "3.10"]
    steps:
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/checkout@v3
      - run: pip3 install .[ci]
      - run: python3 -m pytest test
        name: Test building EMFFAX pages
