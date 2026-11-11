"""Command-line entry point:  python -m statval data.csv [options]"""
import argparse
import sys

from . import __version__
from .loader import load_csv, split_columns
from .metrics import describe_numeric, describe_categorical, correlation_flags
from .report import FORMATTERS


def analyse(df, path, alpha=0.05, corr_threshold=0.8):
    numeric, categorical = split_columns(df)
    result = {"file": path, "rows": len(df), "columns": df.shape[1],
              "numeric": {c: describe_numeric(df[c], alpha) for c in numeric},
              "categorical": {c: describe_categorical(df[c]) for c in categorical},
              "flags": []}
    for c, m in result["numeric"].items():
        if m.get("missing"):
            result["flags"].append(f"{c}: {m['missing']} missing value(s)")
        if m.get("outliers"):
            result["flags"].append(f"{c}: {m['outliers']} IQR outlier(s)")
        if m.get("normality") == "non-normal":
            result["flags"].append(f"{c}: not normal (Shapiro p = {m['shapiro_p']:.4f})")
        if m.get("skewness") is not None and abs(m["skewness"]) > 1:
            result["flags"].append(f"{c}: highly skewed ({m['skewness']:.2f})")
    for c, m in result["categorical"].items():
        if m["missing"]:
            result["flags"].append(f"{c}: {m['missing']} missing value(s)")
    for a, b, r in correlation_flags(df, numeric, corr_threshold):
        result["flags"].append(f"{a} ~ {b}: strong correlation (r = {r:.2f})")
    return result


def build_parser():
    p = argparse.ArgumentParser(prog="statval",
        description="Compute statistical metrics and validation flags for a CSV dataset.")
    p.add_argument("csv", help="path to the CSV file")
    p.add_argument("-c", "--columns", nargs="+", help="only analyse these columns")
    p.add_argument("-f", "--format", choices=FORMATTERS, default="text", help="output format (default: text)")
    p.add_argument("-o", "--output", help="write the report to this file instead of the screen")
    p.add_argument("--alpha", type=float, default=0.05, help="significance level for the normality test")
    p.add_argument("--corr", type=float, default=0.8, help="flag column pairs with |r| above this")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        df = load_csv(args.csv, args.columns)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    report = FORMATTERS[args.format](analyse(df, args.csv, args.alpha, args.corr))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(report + "\n")
        print(f"Report written to {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
