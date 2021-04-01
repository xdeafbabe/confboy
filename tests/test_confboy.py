import pytest

import confboy


def test_confboy_get_and_set_values():
    config = confboy.Config()
    config.key = 'value'

    assert config.key == 'value'


def test_confboy_get_nonexistent_value():
    config = confboy.Config()

    with pytest.raises(KeyError):
        config.nonexistent_key


def test_confboy_merge_configs():
    config = confboy.Config()
    config.merge_config({'key_1': 'value_1', 'key_2': 'value_2'})

    assert config.key_1 == 'value_1'
    assert config.key_2 == 'value_2'


def test_confboy_merge_nested_configs():
    config = confboy.Config()
    config.merge_config({
        'outer': {
            'inner': 'value',
        },
    })

    assert config.outer.inner == 'value'


def test_confboy_merge_nested_configs_with_nested_config():
    config = confboy.Config()
    config.merge_config({
        'outer': {
            'inner_1': 'value_1',
            'inner_2': 'outdated',
        },
        'outer_1': 'outer_value_1',
        'outer_2': 'outdated',
    })

    config.merge_config({
        'outer': {
            'inner_2': 'value_2',
            'inner_3': 'value_3',
        },
        'outer_2': 'outer_value_2',
    })

    assert config.outer.inner_1 == 'value_1'
    assert config.outer.inner_2 == 'value_2'
    assert config.outer.inner_3 == 'value_3'
    assert config.outer_1 == 'outer_value_1'
    assert config.outer_2 == 'outer_value_2'
