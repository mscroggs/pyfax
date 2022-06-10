import pyfax


def test_config():
    assert pyfax.config.hello is None
    pyfax.config.hello = "VALUE"
    assert pyfax.config.hello == "VALUE"
