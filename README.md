# statval: Statistical Validation CLI

A command-line tool that reads any CSV dataset, computes foundational statistical metrics, runs validation checks, and prints a clean report as text, Markdown or JSON.

## What it computes
- **Numeric columns:** count, missing, mean, median, mode, standard deviation, variance, min, Q1, Q3, max, IQR, skewness, excess kurtosis, IQR outliers, Shapiro-Wilk normality test
- **Categorical columns:** count, missing, unique values, most frequent value
- **Validation flags:** missing values, outliers, non-normal columns, high skew (|skew| > 1), strongly correlated column pairs (|r| >= 0.8)

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
python -m statval data/iris.csv                                     # text report on screen
python -m statval data/mtcars.csv -c mpg wt hp                      # only some columns
python -m statval data/mtcars.csv -f markdown -o reports/mtcars.md  # save a Markdown report
python -m statval data/iris.csv -f json                             # JSON for other programs
python -m statval --help
```

| Option | Meaning |
|---|---|
| `-c, --columns` | analyse only these columns |
| `-f, --format` | `text` (default), `markdown` or `json` |
| `-o, --output` | write the report to a file |
| `--alpha` | significance level for the normality test (default 0.05) |
| `--corr` | correlation threshold for flags (default 0.8) |

## Project structure
```
statval/
  loader.py    # read CSV, split numeric / categorical columns
  metrics.py   # one function per statistic
  report.py    # text, Markdown and JSON formatters
  cli.py       # argparse interface and validation flags
tests/
  test_statval.py   # pytest unit tests
data/
  iris.csv, mtcars.csv   # sample datasets
```

## Tests
```bash
python -m pytest -q
```

Author: Khushi, MSc Data Science & Analytics, Jain University
