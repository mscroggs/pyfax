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
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.10"
      - run: pip3 install .[ci]
      - run: python3 -m pytest test
        name: Test building EMFFAX pages
