"""Format results as a text report, Markdown or JSON."""
import json

NUM_COLS = ["n", "missing", "mean", "median", "std", "min", "max", "iqr",
            "skewness", "kurtosis", "outliers", "normality"]


def _fmt(v):
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


def _table(rows, headers):
    widths = [max(len(h), *(len(_fmt(r.get(h, ""))) for r in rows)) for h in headers]
    line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    out = [line, "-" * len(line)]
    for r in rows:
        out.append("  ".join(_fmt(r.get(h, "")).ljust(w) for h, w in zip(headers, widths)))
    return "\n".join(out)


def _numeric_rows(result):
    return [{"column": c, **m} for c, m in result["numeric"].items()]


def to_text(result):
    lines = [f"STATISTICAL VALIDATION REPORT: {result['file']}",
             f"Rows: {result['rows']}  |  Columns: {result['columns']}  |  "
             f"Numeric: {len(result['numeric'])}  |  Categorical: {len(result['categorical'])}", ""]
    if result["numeric"]:
        lines += ["NUMERIC COLUMNS", _table(_numeric_rows(result), ["column"] + NUM_COLS), ""]
    if result["categorical"]:
        rows = [{"column": c, **m} for c, m in result["categorical"].items()]
        lines += ["CATEGORICAL COLUMNS", _table(rows, ["column", "n", "missing", "unique", "top", "top_freq"]), ""]
    lines.append("VALIDATION FLAGS")
    lines += [f"  - {f}" for f in result["flags"]] or ["  - none"]
    return "\n".join(lines)


def to_markdown(result):
    out = [f"# Statistical validation report: `{result['file']}`", "",
           f"**Rows:** {result['rows']} | **Columns:** {result['columns']}", ""]
    if result["numeric"]:
        hdr = ["column"] + NUM_COLS
        out += ["## Numeric columns", "", "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
        out += ["| " + " | ".join(_fmt(r.get(h, "")) for h in hdr) + " |" for r in _numeric_rows(result)]
        out.append("")
    if result["categorical"]:
        hdr = ["column", "n", "missing", "unique", "top", "top_freq"]
        out += ["## Categorical columns", "", "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
        out += ["| " + " | ".join(_fmt(m.get(h, c if h == "column" else "")) for h in hdr) + " |"
                for c, m in result["categorical"].items()]
        out.append("")
    out += ["## Validation flags", ""] + ([f"- {f}" for f in result["flags"]] or ["- none"])
    return "\n".join(out)


def to_json(result):
    return json.dumps(result, indent=2, default=str)


FORMATTERS = {"text": to_text, "markdown": to_markdown, "json": to_json}
