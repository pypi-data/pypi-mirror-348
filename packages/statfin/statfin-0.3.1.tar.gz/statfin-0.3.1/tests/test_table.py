import pytest
import statfin


StatFin = statfin.StatFin()


def test_variable_access():
    table = StatFin.tyokay._115b
    assert isinstance(table, statfin.Table)

    assert isinstance(table.Alue, statfin.Variable)
    assert isinstance(table["Alue"], statfin.Variable)
    assert isinstance(table.Alue.SSS, statfin.Value)
    assert isinstance(table.Alue["SSS"], statfin.Value)
