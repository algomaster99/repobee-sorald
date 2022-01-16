from _repobee import plugin

from repobee_sorald import sorald


def test_register():
    """Just test that there is no crash"""
    plugin.register_plugins([sorald])
