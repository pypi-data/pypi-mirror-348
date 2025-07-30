from datetime import datetime

import pytest

import numpy as np
import statfin


def test_time_parsing():
    assert statfin.parse.time("2002") == datetime(2002, 1, 1)
    assert statfin.parse.time("2023M04") == datetime(2023, 4, 1)
    assert statfin.parse.time("2023M12") == datetime(2023, 12, 1)
    assert statfin.parse.time("1999Q1") == datetime(1999, 1, 1)
    assert statfin.parse.time("1999Q2") == datetime(1999, 4, 1)
    assert statfin.parse.time("1999Q3") == datetime(1999, 7, 1)
    assert statfin.parse.time("1999Q4") == datetime(1999, 10, 1)


def test_number_or_nan_parsing():
    assert statfin.parse.number_or_nan("1") == 1.0
    assert statfin.parse.number_or_nan("2.0") == 2.0
    assert statfin.parse.number_or_nan("3,13") == 3.13
    assert statfin.parse.number_or_nan("2300.5") == 2_300.5
    assert np.isnan(statfin.parse.number_or_nan(""))
    assert np.isnan(statfin.parse.number_or_nan("."))
    assert np.isnan(statfin.parse.number_or_nan(".."))
    assert np.isnan(statfin.parse.number_or_nan("-"))


def test_number_or_raw_parsing():
    assert statfin.parse.number_or_raw("1") == 1.0
    assert statfin.parse.number_or_raw("2.0") == 2.0
    assert statfin.parse.number_or_raw("3,13") == 3.13
    assert statfin.parse.number_or_raw("2300.5") == 2_300.5
    assert statfin.parse.number_or_raw("") == ""
    assert statfin.parse.number_or_raw(".") == "."
    assert statfin.parse.number_or_raw("..") == ".."
    assert statfin.parse.number_or_raw("-") == "-"
