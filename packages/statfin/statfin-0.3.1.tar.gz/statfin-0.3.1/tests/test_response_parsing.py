from datetime import datetime

import pytest
import numpy as np

import statfin
from statfin.table_response import TableResponse


def test_handles_different_data_formats():
    response = TableResponse(
        {
            "columns": [
                {"code": "Time", "text": "Time", "type": "t"},
                {"code": "Value", "text": "Value", "type": "c"},
            ],
            "data": [
                {"key": ["2000"], "values": ["1.0"]},
                {"key": ["2001"], "values": ["2 400,50"]},
                {"key": ["2002"], "values": ["."]},
                {"key": ["2003"], "values": [".."]},
                {"key": ["2004"], "values": ["-"]},
            ],
        }
    )
    assert response.df.iloc[0].Value == 1.0
    assert response.df.iloc[1].Value == 2_400.50
    assert np.isnan(response.df.iloc[2].Value)
    assert np.isnan(response.df.iloc[3].Value)
    assert np.isnan(response.df.iloc[4].Value)


def test_ehi_ge():
    response = TableResponse(
        {
            "columns": [
                {"code": "Kuukausi", "text": "Kuukausi", "type": "t"},
                {"code": "Polttoneste", "text": "Polttoneste", "type": "d"},
                {"code": "hinta", "text": "Hinta", "type": "c"},
                {
                    "code": "vuosimuutos_hinta",
                    "text": "Hinta, vuosimuutos (%)",
                    "type": "c",
                },
            ],
            "comments": [],
            "data": [
                {"key": ["1988M01", "A"], "values": ["56.0", "."]},
                {"key": ["1988M01", "B"], "values": ["40.0", "."]},
                {"key": ["1988M01", "C"], "values": ["16.0", "."]},
                {"key": ["1988M01", "D"], "values": ["16.1", "."]},
                {"key": ["1989M05", "A"], "values": ["61.4", "9.0"]},
            ],
        }
    )

    assert len(response.columns.dimensions) == 2
    assert response.columns.dimensions[0].code == "Kuukausi"
    assert response.columns.dimensions[0].time == True
    assert response.columns.dimensions[1].code == "Polttoneste"
    assert response.columns.dimensions[1].time == False

    assert len(response.columns.measures) == 2
    assert response.columns.measures[0].code == "hinta"
    assert response.columns.measures[1].code == "vuosimuutos_hinta"

    assert len(response.df), 5

    assert response.df.iloc[0].Kuukausi == datetime(1988, 1, 1)
    assert response.df.iloc[0].Polttoneste == "A"
    assert response.df.iloc[0].hinta == 56.0
    assert np.isnan(response.df.iloc[0].vuosimuutos_hinta)

    assert response.df.iloc[4].Kuukausi == datetime(1989, 5, 1)
    assert response.df.iloc[4].Polttoneste == "A"
    assert response.df.iloc[4].hinta == 61.4
    assert response.df.iloc[4].vuosimuutos_hinta == 9.0
