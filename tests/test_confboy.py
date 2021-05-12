import pathlib

import pytest

import confboy


def test_get_and_set_values():
    config = confboy.Config()
    config.key = 'value'

    assert config.key == 'value'


def test_get_nonexistent_value():
    config = confboy.Config()

    with pytest.raises(KeyError):
        config.nonexistent_key


def test_merge_configs():
    config = confboy.Config()
    config.merge_config({'key_1': 'value_1', 'key_2': 'value_2'})

    assert config.key_1 == 'value_1'
    assert config.key_2 == 'value_2'


def test_merge_nested_configs():
    config = confboy.Config()
    config.merge_config({
        'outer': {
            'inner': 'value',
        },
    })

    assert config.outer.inner == 'value'


def test_merge_nested_configs_with_nested_config():
    config = confboy.Config()
    config.merge_config({
        'outer': {
            'inner_1': 'value_1',
            'inner_2': 'outdated',
        },
        'outer_1': 'outer_value_1',
        'outer_2': 'outdated',
        'nested': False,
    })

    config.merge_config({
        'outer': {
            'inner_2': 'value_2',
            'inner_3': 'value_3',
        },
        'outer_2': 'outer_value_2',
        'nested': {
            'key': 'value',
        },
    })

    assert config.outer.inner_1 == 'value_1'
    assert config.outer.inner_2 == 'value_2'
    assert config.outer.inner_3 == 'value_3'
    assert config.outer_1 == 'outer_value_1'
    assert config.outer_2 == 'outer_value_2'
    assert config.nested.key == 'value'


def test_set_nested_value():
    config = confboy.Config()
    config.nested = {'one': 1, 'two': 2}

    assert config.nested.one == 1
    assert config.nested.two == 2


def test_delete_config_key():
    config = confboy.Config()
    config.key = 'value'
    del config.key

    with pytest.raises(KeyError):
        config.key


def test_callables():
    config = confboy.Config({
        'a': {'a': 1},
        'b': 2,
        'a_plus_b': 'callable:add',
    })

    def add():
        return config.a.a + config.b

    config.register_callable(add)

    assert config.a_plus_b == 3


def test_merge_toml_config():
    path = str(pathlib.Path(__file__).parent.absolute() / 'test_config.toml')
    config = confboy.Config(toml_config_path=path)

    assert config.key == 'value'
    assert config.nested.one == 1
    assert config.nested.two == 2


def test_merge_invalid_toml_config():
    path = str(
        pathlib.Path(__file__).parent.absolute() / 'test_invalid_config.toml')

    with pytest.raises(confboy.InvalidConfigFileError):
        confboy.Config(toml_config_path=path)


def test_merge_nonexistent_toml_config():
    config = confboy.Config(toml_config_path='/nonexistent_file')
    assert config._config == {}
