from datetime import datetime
import re

import numpy as np


def _number_to_str(x: str) -> float:
    x = x.strip()
    x = x.replace(",", ".")  # Undo comma decimal separator
    x = x.replace(" ", "")  # Undo extra spaces
    return float(x)


def number_or_nan(x) -> float:
    try:
        return _number_to_str(str(x))
    except ValueError:
        return float(np.nan)


def number_or_raw(x) -> float:
    try:
        return _number_to_str(str(x))
    except ValueError:
        return x


def time(x: str) -> datetime | str:
    x = x.strip()
    if re.fullmatch(r"\d{4}", x):
        return datetime.strptime(x, "%Y")
    elif re.fullmatch(r"\d{4}M\d{2}", x):
        return datetime.strptime(x, "%YM%m")
    elif re.fullmatch(r"\d{4}Q\d", x):
        y, q = x.split("Q")
        return datetime(int(y), 3 * int(q) - 2, 1)
    elif re.fullmatch(r"\d{4}-\d{2}", x):
        return datetime.strptime(x, "%Y-%m")
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", x):
        return datetime.strptime(x, "%Y-%m-%d")
    else:
        return x
