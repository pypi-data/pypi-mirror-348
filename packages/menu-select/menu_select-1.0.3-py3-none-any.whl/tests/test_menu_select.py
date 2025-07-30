import pytest
from menu_select.Menu_select import Menu_select as ms
# from menu_select.Menu_select import Menu_select as ms

def test_menu_select_valid_choice():
    options = ["Option 1", "Option 2", "Option 3"]
    menu = ms("cabeçalho")
    result = menu.options(opções=options)
    assert (result == 0 or result == 1 or result == 2), "Expected a valid choice (0, 1, or 2) but got: {}".format(result)