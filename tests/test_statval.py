import json
import pandas as pd
import pytest
from statval import metrics
from statval.cli import analyse, main


def test_basic_metrics():
    s = pd.Series([1, 2, 3, 4, 100])
    assert metrics.mean(s) == 22
    assert metrics.median(s) == 3
    assert metrics.iqr_outliers(s) == 1


def test_missing_values_counted():
    m = metrics.describe_numeric(pd.Series([1.0, None, 3.0]))
    assert m["n"] == 2 and m["missing"] == 1


def test_correlation_flag():
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 4, 6, 8], "c": [4, 1, 3, 2]})
    pairs = metrics.correlation_flags(df, ["a", "b", "c"])
    assert pairs[0][:2] == ("a", "b")


def test_analyse_flags_outlier():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 100], "g": list("aabbc")})
    r = analyse(df, "t.csv")
    assert any("outlier" in f for f in r["flags"])
    assert r["categorical"]["g"]["unique"] == 3


def test_cli_json(tmp_path, capsys):
    p = tmp_path / "d.csv"
    pd.DataFrame({"x": [1, 2, 3, 4]}).to_csv(p, index=False)
    assert main([str(p), "-f", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["rows"] == 4


def test_cli_bad_column(tmp_path):
    p = tmp_path / "d.csv"
    pd.DataFrame({"x": [1, 2]}).to_csv(p, index=False)
    assert main([str(p), "-c", "nope"]) == 1
