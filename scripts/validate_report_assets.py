"""Kontrola wartości wykresów, eksportów i powiązań w pisemnej pracy."""

import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from decimal import Decimal as D
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def csv_rows(relative):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    manifest = json.loads((ROOT / "reports/figures_manifest.json").read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "reports/trade_output_validation.json").read_text(encoding="utf-8"))
    assert all(audit["analysis_csv_sha256"].get(k)==v for k,v in manifest["input_sha256"].items())
    for relative, digest in audit["analysis_csv_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    summary = {row["entry_rule"]: row for row in csv_rows("data/analysis/summary_by_rule_90d.csv")}
    event_summary = {row["entry_rule"]: row for row in csv_rows("data/analysis/summary_event_means_90d.csv")}
    events = {(row["event_id"], row["entry_rule"]): row for row in csv_rows("data/analysis/event_mean_returns_90d.csv")}
    chart_data = csv_rows(manifest["chart_data_path"])
    assert len(chart_data) == manifest["chart_values"] == 93
    errors = []
    keys = set()
    for row in chart_data:
        rule, series, figure = row["entry_rule"], row["series"], row["figure"]
        key = (figure, rule, row["event_id"], series)
        assert key not in keys
        keys.add(key)
        if figure in ("01_stopy_zwrotu", "04_ryzyko_pozycji"):
            expected = D(summary[rule][series]) * 100
            assert row["denominator"] == "100" and row["unit"] == "percent"
        elif figure == "02_zysk_i_przewaga_koszykow":
            expected = D(event_summary[rule][series + "_count"]) / D(20) * 100
            assert row["denominator"] == "20" and row["unit"] == "percent"
        else:
            assert figure == "03_przewaga_w_kazdym_zdarzeniu"
            expected = D(events[(row["event_id"], rule)]["advantage_net_pp"])
            assert row["denominator"] == "5" and row["unit"] == "percentage_points"
        error = abs(expected - D(row["value"]))
        assert error < D("1e-10"), key
        errors.append(error)
    assert len(manifest["files"]) == 8
    dimensions = {}
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], entry["path"]
        if path.suffix == ".svg":
            assert ET.parse(path).getroot().tag.endswith("svg")
        else:
            with Image.open(path) as picture:
                picture.verify()
            with Image.open(path) as picture:
                assert picture.width >= 2000 and picture.height >= 1200
                dimensions[entry["path"]] = list(picture.size)
    report_path = ROOT / "raport/RAPORT.md"
    report = report_path.read_text(encoding="utf-8")
    links = re.findall(r"!\[([^\]]+)\]\(<([^>]+)>\)", report)
    assert len(links) == 5 and len({path for _, path in links}) == 5
    for alt_text, target in links:
        assert alt_text.strip() and (report_path.parent / target).is_file(), target
    assert re.findall(r"^# ([1-6])\. ", report, re.MULTILINE) == ["1", "2", "3", "4", "5", "6"]
    assert "# Streszczenie" in report and report.index("# Streszczenie") < report.index("# 1.")
    assert "## Narzędzia i sposób pracy" in report and "## Instrukcja odtworzenia z zachowanych źródeł" in report
    assert not any(phrase in report for phrase in ("Wyniki przedstawimy", "W zestawieniach pokażemy", "Sukces wyniku A:", "Uwaga do późniejszej metodologii"))
    for rule in ("A", "B", "C"):
        expected = f"{D(summary[rule]['median_alt_net_return']) * 100:.2f}".replace(".", ",") + "%"
        abstract = (ROOT / "raport/00_streszczenie.md").read_text(encoding="utf-8")
        assert expected in abstract, ("Abstract median does not match validated data", rule)
    assert len(re.findall(r"\*\*Wykres [1-5]\.", report)) == 5
    drawdown_manifest = json.loads((ROOT / 'reports/drawdown_figure_manifest.json').read_text(encoding='utf-8'))
    for entry in drawdown_manifest['files']:
        assert hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    risk_summary = csv_rows('data/analysis/summary_basket_capital_risk_90d.csv')
    for row in risk_summary:
        for field in ('median_alt_mdd', 'median_btc_mdd', 'worst_alt_mdd', 'worst_btc_mdd'):
            expected = f"{D(row[field]) * 100:.2f}%".replace('.', ',').replace('-', '−')
            assert expected in report, (row['entry_rule'], field, expected)
    result = {"status": "passed", "analysis_csv_hashes_unchanged": len(audit["analysis_csv_sha256"]),
              "chart_values_checked": len(chart_data), "max_plot_value_error": str(max(errors)),
              "verified_exports": len(manifest["files"]), "png_dimensions": dimensions,
              "svg_xml_valid": True, "report_image_links_checked": len(links), "report_chapters": 6,
              "abstract_before_chapters": True, "abstract_medians_match_data": True,
              "manual_visual_review": "Recorded separately in the project diary; this script checks numbers, file integrity and document references.",
              "report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest()}
    (ROOT / "reports/report_assets_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
