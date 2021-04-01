import confboy


def test_confboy():
    config = confboy.Config()
    assert isinstance(config, confboy.Config)
