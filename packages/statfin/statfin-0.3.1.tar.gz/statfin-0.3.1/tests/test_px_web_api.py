import pytest
import statfin


Vero = statfin.Vero()
StatFin = statfin.StatFin()


def test_Vero():
    assert isinstance(Vero, statfin.PxWebAPI)
    assert Vero.url == "https://vero2.stat.fi/PXWeb/api/v1/fi"


def test_StatFin():
    assert isinstance(StatFin, statfin.PxWebAPI)
    assert StatFin.url == "https://statfin.stat.fi/PXWeb/api/v1/fi"


def test_attribute_access():
    assert isinstance(StatFin.StatFin, statfin.PxWebAPI)
    assert isinstance(StatFin.StatFin.khi, statfin.PxWebAPI)
    assert isinstance(StatFin.StatFin.khi.statfin_khi_pxt_11xb, statfin.Table)


def test_attribute_access_abbreviated():
    assert isinstance(StatFin.StatFin, statfin.PxWebAPI)
    assert isinstance(StatFin.StatFin.khi, statfin.PxWebAPI)
    assert isinstance(StatFin.StatFin.khi._11xb, statfin.Table)


def test_attribute_access_abbreviated_2():
    assert isinstance(Vero.Vero.Henk.lop.tulot, statfin.PxWebAPI)
    assert isinstance(Vero.Vero.Henk.lop.tulot._101, statfin.Table)


def test_indexing():
    assert isinstance(StatFin["StatFin"], statfin.PxWebAPI)
    assert isinstance(StatFin["StatFin"]["khi"], statfin.PxWebAPI)
    assert isinstance(StatFin["StatFin"]["khi"]["statfin_khi_pxt_11xb"], statfin.Table)


def test_indexing_abbreviated():
    assert isinstance(StatFin["StatFin"], statfin.PxWebAPI)
    assert isinstance(StatFin["StatFin"]["khi"], statfin.PxWebAPI)
    assert isinstance(StatFin["StatFin"]["khi"]["_11xb"], statfin.Table)


def test_attribute_access_using_default_database():
    assert isinstance(StatFin.khi, statfin.PxWebAPI)
    assert isinstance(StatFin.khi._11xb, statfin.Table)


def test_attribute_access_using_default_database_2():
    assert isinstance(Vero.Henk, statfin.PxWebAPI)
    assert isinstance(Vero.Henk.lop.tulot._101, statfin.Table)
