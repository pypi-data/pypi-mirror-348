import os
import pandas as pd
import pytest
import statfin


Vero = statfin.Vero()
StatFin = statfin.StatFin()


def test_query():
    table = StatFin.tyokay._115b
    assert isinstance(table, statfin.Table)

    q = table.query(Alue="SSS", Tiedot="vaesto")
    q["Pääasiallinen toiminta"] = "*"  # All values
    q.Vuosi = 2023  # Single value (will be cas to str)
    q.Sukupuoli = [1, 2]  # Multiple values
    q.Ikä = "18-64"  # Single value
    df = q()
    assert isinstance(df, pd.DataFrame)


def test_cached_query():
    statfin.cache.clear()
    table = StatFin.tyokay._115b
    assert isinstance(table, statfin.Table)

    q = table.query(Alue="SSS", Tiedot="vaesto")
    df = q("test")  # With cache id "test"
    assert isinstance(df, pd.DataFrame)
    assert os.path.isfile(".statfin_cache/test.df")
    assert os.path.isfile(".statfin_cache/test.meta")

    df = q("test")
    assert isinstance(df, pd.DataFrame)
