"""Cztery wykresy raportowe z walidowanych CSV; eksport PNG i SVG."""

import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_LIBS = ROOT / ".dependencies/plotting"
if LOCAL_LIBS.exists():
    sys.path.insert(0, str(LOCAL_LIBS))
os.environ["MPLCONFIGDIR"] = str(ROOT / ".cache/matplotlib")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.ticker import FuncFormatter, MultipleLocator

OUT = ROOT / "raport/wykresy"
ALT, BTC, MUTED = "#166C88", "#C57126", "#66758A"
INK, GRID = "#172D3D", "#DCE3E8"
RULES = ("A", "B", "C")
LABELS = ["A · D+1", "B · D+7", "C · powrót RSI"]
SOURCE = "Opracowanie własne · ceny: Binance / KuCoin · rankingi: Data: CryptWatch, based on CoinMarketCap"
COSTS = "90 dni · USDT · prowizja 0,10% i poślizg 0,05% przy zakupie oraz sprzedaży"
DATA_FOR_PLOTS = []
FILES = []


def read_csv(relative):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def pl(value, digits=1):
    return f"{value:.{digits}f}".replace(".", ",").replace("-", "−")


def percent_tick(value, _position):
    return pl(value, 0) + "%"


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11, "text.color": INK,
        "axes.labelcolor": INK, "axes.edgecolor": GRID, "xtick.color": INK, "ytick.color": INK,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "axes.spines.bottom": False, "figure.facecolor": "white", "axes.facecolor": "white",
        "svg.fonttype": "none", "svg.hashsalt": "google-da-altcoins-90d-v1", "savefig.facecolor": "white",
        "axes.titleweight": "bold", "axes.titlesize": 12, "legend.frameon": False,
    })


def heading(fig, title, subtitle):
    fig.text(0.07, 0.958, title, va="top", fontsize=18, fontweight="bold")
    fig.text(0.07, 0.907, subtitle, va="top", fontsize=10.5, color=MUTED)


def footer(fig, notes):
    fig.text(0.07, 0.095, notes, fontsize=9, color=MUTED, va="top", linespacing=1.5)
    fig.text(0.07, 0.023, SOURCE, fontsize=8, color=MUTED, va="bottom")


def save(fig, slug, title, sources, unit, notes):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    texts = list(fig.texts)
    legends = list(fig.legends)
    for ax in fig.axes:
        xmin, xmax = sorted(ax.get_xlim())
        ymin, ymax = sorted(ax.get_ylim())
        xticks = [item for item in ax.get_xticklabels() if xmin <= item.get_position()[0] <= xmax]
        yticks = [item for item in ax.get_yticklabels() if ymin <= item.get_position()[1] <= ymax]
        texts.extend([ax.title, ax.xaxis.label, ax.yaxis.label, *ax.texts, *xticks, *yticks])
        if ax.get_legend() is not None:
            legends.append(ax.get_legend())
    for item in texts:
        if item.get_visible() and item.get_text():
            box = item.get_window_extent(renderer)
            assert box.x0 >= -1 and box.y0 >= -1 and box.x1 <= fig.bbox.width + 1 and box.y1 <= fig.bbox.height + 1, (slug, item.get_text(), box)
    for legend in legends:
        for header in fig.texts[:2]:
            assert not legend.get_window_extent(renderer).overlaps(header.get_window_extent(renderer)), (slug, "Legend overlaps header")
    for extension in ("png", "svg"):
        target = OUT / f"{slug}.{extension}"
        kwargs = {"metadata": {"Title": title, "Description": notes, "Date": None}} if extension == "svg" else {"metadata": {"Title": title, "Description": notes}}
        fig.savefig(target, dpi=200, **kwargs)
        FILES.append({"path": target.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                      "title": title, "sources": sources, "unit": unit, "notes": notes})
    plt.close(fig)


def record(figure, rule, series, value, unit, denominator, event_id=""):
    DATA_FOR_PLOTS.append({"figure": figure, "entry_rule": rule, "event_id": event_id, "series": series,
                           "value": value, "unit": unit, "denominator": denominator})


def return_comparison(summary):
    slug = "01_stopy_zwrotu"
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.4))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.75, bottom=0.24, wspace=0.28)
    heading(fig, "Zysk altcoinów nie oznaczał przewagi nad BTC", "Wyniki pojedynczych pozycji · 100 dopasowanych par na regułę, z 20 wspólnych sygnałów")
    x = np.arange(3)
    for ax, statistic, title in zip(axes, ("mean", "median"), ("Średnia netto", "Mediana netto")):
        for offset, prefix, color, label in ((-0.19, "alt", ALT, "Altcoiny"), (0.19, "btc", BTC, "Dopasowany BTC")):
            values = [100 * float(summary[rule][f"{statistic}_{prefix}_net_return"]) for rule in RULES]
            bars = ax.bar(x + offset, values, width=0.34, color=color, label=label, zorder=3)
            ax.bar_label(bars, labels=[pl(value, 2) + "%" for value in values], padding=5, fontsize=10)
            for rule, value in zip(RULES, values):
                record(slug, rule, statistic + "_" + prefix + "_net_return", value, "percent", 100)
        ax.set_title(title, loc="left", pad=17)
        ax.set_xticks(x, LABELS, fontsize=10)
        ax.set_ylim(0, 13.5)
        ax.yaxis.set_major_formatter(FuncFormatter(percent_tick))
        ax.yaxis.set_major_locator(MultipleLocator(3))
        ax.grid(axis="y", color=GRID, zorder=0)
        ax.tick_params(length=0, pad=9)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.07, 0.865), ncol=2, fontsize=10, borderaxespad=0)
    footer(fig, COSTS + "\nBTC: ta sama giełda i te same daty co altcoin. Pary nie są niezależnymi próbami.")
    save(fig, slug, "Zysk altcoinów nie oznaczał przewagi nad BTC", ["data/analysis/summary_by_rule_90d.csv"], "percent",
         "Mean and median individual net returns; 100 paired trades per rule from 20 signals. No confidence intervals or independence assumption.")


def event_success(summary):
    slug = "02_zysk_i_przewaga_koszykow"
    fig, ax = plt.subplots(figsize=(12, 6.4))
    fig.subplots_adjust(left=0.19, right=0.94, top=0.72, bottom=0.24)
    heading(fig, "Koszyk pokonał BTC w 4–5 z 20 zdarzeń", "Pięć monet · równe początkowe udziały po 20% · osobny hipotetyczny budżet dla każdego sygnału")
    positions = np.arange(3)
    for offset, field, label, color in ((-0.23, "success_profit", "Zysk po kosztach", ALT),
                                       (0, "success_btc", "Przewaga nad BTC", BTC),
                                       (0.23, "success_both", "Zysk i przewaga", MUTED)):
        values = [float(summary[rule][field + "_pct"]) for rule in RULES]
        bars = ax.barh(positions + offset, values, height=0.19, color=color, label=label, zorder=3)
        labels = [f"{summary[rule][field + '_count']}/20 ({pl(value, 0)}%)" for rule, value in zip(RULES, values)]
        ax.bar_label(bars, labels=labels, padding=7, fontsize=10)
        for rule, value in zip(RULES, values):
            record(slug, rule, field, value, "percent", 20)
    ax.set_yticks(positions, LABELS)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(FuncFormatter(percent_tick))
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.grid(axis="x", color=GRID, zorder=0)
    ax.tick_params(length=0, pad=10)
    ax.legend(loc="upper left", bbox_to_anchor=(0, 1.25), ncol=3, fontsize=10)
    footer(fig, COSTS + "\nZestawienie opisowe dodane po wynikach indywidualnych. Bez łączenia kapitału między sygnałami.")
    save(fig, slug, "Koszyk pokonał BTC w 4–5 z 20 zdarzeń", ["data/analysis/summary_event_means_90d.csv"], "percent",
         "Event-level success frequencies out of 20. Equal 20% initial weights; benchmark is the mean of five venue-matched BTC returns. Supplemental descriptive aggregation.")


def event_heatmap(rows):
    slug = "03_przewaga_w_kazdym_zdarzeniu"
    signals = sorted({row["signal_date"] for row in rows})
    index = {(row["signal_date"], row["entry_rule"]): row for row in rows}
    values = np.array([[float(index[(day, rule)]["advantage_net_pp"]) for rule in RULES] for day in signals])
    limit = math.ceil(float(np.abs(values).max()) / 10) * 10
    fig, ax = plt.subplots(figsize=(10.5, 10.2))
    fig.subplots_adjust(left=0.23, right=0.82, top=0.84, bottom=0.18)
    heading(fig, "Przewaga koszyka nad BTC w każdym zdarzeniu", "Średnia pięciu wyników netto minus średnia dopasowanego BTC · punkty procentowe")
    cmap = LinearSegmentedColormap.from_list("loss_neutral_gain", ["#A44A18", "#F4F4EF", "#11627E"])
    picture = ax.imshow(values, cmap=cmap, norm=TwoSlopeNorm(vcenter=0, vmin=-limit, vmax=limit), aspect="auto")
    ax.set_xticks(np.arange(3), LABELS)
    ax.xaxis.tick_top()
    ax.set_yticks(np.arange(len(signals)), signals, fontsize=10)
    ax.tick_params(length=0, pad=12)
    for i, day in enumerate(signals):
        for j, rule in enumerate(RULES):
            value = values[i, j]
            ax.text(j, i, pl(value), ha="center", va="center", fontsize=10.5,
                    color="white" if abs(value) > limit * 0.6 else INK)
            record(slug, rule, "event_advantage_net_pp", value, "percentage_points", 5, index[(day, rule)]["event_id"])
    boundary = sum(day < "2023-01-01" for day in signals) - 0.5
    ax.axhline(boundary, color=INK, linewidth=1.5, linestyle=(0, (3, 3)))
    ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(signals), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    cax = fig.add_axes([0.86, 0.29, 0.025, 0.44])
    colorbar = fig.colorbar(picture, cax=cax)
    colorbar.ax.set_title("p.p.", fontsize=10, pad=10)
    colorbar.outline.set_visible(False)
    colorbar.ax.tick_params(length=0)
    footer(fig, "Wartość dodatnia: koszyk lepszy od BTC; ujemna: BTC lepszy. Każdy wiersz to jeden sygnał.\nLinia oddziela okresy 2020–2022 i 2023–2025. Sygnały i ich okresy utrzymywania są powiązane.\n" + COSTS)
    save(fig, slug, "Przewaga koszyka nad BTC w każdym zdarzeniu", ["data/analysis/event_mean_returns_90d.csv"], "percentage_points",
         "All 20 events, three entry rules. Equal initial asset weights; BTC benchmark uses matching venue weights. Diverging symmetric scale, no clipping or cumulative-wealth interpretation.")


def risk_comparison(summary):
    slug = "04_ryzyko_pozycji"
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.4))
    fig.subplots_adjust(left=0.17, right=0.98, top=0.72, bottom=0.25, wspace=0.36)
    heading(fig, "Altcoiny miały głębsze mediany spadków cen", "Ryzyko pojedynczych pozycji · 100 par na regułę z 20 sygnałów · miary cenowe bez kosztów")
    y = np.arange(3)
    for ax, field, title in zip(axes, ("mae", "mdd_close"), ("Spadek względem wejścia · MAE", "Obsunięcie od szczytu · MDD")):
        for offset, prefix, color, label in ((-0.18, "alt", ALT, "Altcoiny"), (0.18, "btc", BTC, "Dopasowany BTC")):
            values = [100 * float(summary[rule][f"median_{prefix}_{field}"]) for rule in RULES]
            bars = ax.barh(y + offset, values, height=0.3, color=color, label=label, zorder=3)
            for bar, value in zip(bars, values):
                ax.text(value - 0.7, bar.get_y() + bar.get_height() / 2, pl(value, 2) + "%", ha="right", va="center", fontsize=9)
            for rule, value in zip(RULES, values):
                record(slug, rule, "median_" + prefix + "_" + field, value, "percent", 100)
        ax.set_yticks(y, LABELS, fontsize=10)
        ax.invert_yaxis()
        ax.set_xlim(-46, 0)
        ax.set_xticks([-40, -30, -20, -10, 0])
        ax.xaxis.set_major_formatter(FuncFormatter(percent_tick))
        ax.set_title(title, loc="left", pad=18, fontsize=11)
        ax.grid(axis="x", color=GRID, zorder=0)
        ax.tick_params(length=0, pad=8)
    axes[0].legend(loc="upper left", bbox_to_anchor=(0, 1.35), ncol=2, fontsize=10)
    footer(fig, "MAE: minima dzienne oraz punkty wejścia i wyjścia. MDD: zamknięcia oraz punkty wejścia i wyjścia.\nWartości bardziej ujemne oznaczają większy spadek. To nie jest ryzyko łącznego koszyka.")
    save(fig, slug, "Altcoiny miały głębsze mediany spadków cen", ["data/analysis/summary_by_rule_90d.csv"], "percent",
         "Median individual MAE and close-based MDD; price-only metrics excluding costs. Not basket-level risk, not full intraday MDD.")


def main():
    audit = json.loads((ROOT / "reports/trade_output_validation.json").read_text(encoding="utf-8"))
    assert audit["status"] == "passed"
    for relative, digest in audit["analysis_csv_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    summaries = {row["entry_rule"]: row for row in read_csv("data/analysis/summary_by_rule_90d.csv")}
    event_summaries = {row["entry_rule"]: row for row in read_csv("data/analysis/summary_event_means_90d.csv")}
    event_rows = read_csv("data/analysis/event_mean_returns_90d.csv")
    assert len(event_rows) == 60 and all(row["status"] == "completed" for row in event_rows)
    assert all(int(row["completed_events"]) == 20 for row in event_summaries.values())
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    return_comparison(summaries)
    event_success(event_summaries)
    event_heatmap(event_rows)
    risk_comparison(summaries)
    data_path = OUT / "dane_do_wykresow.csv"
    with data_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(DATA_FOR_PLOTS[0]))
        writer.writeheader()
        writer.writerows(DATA_FOR_PLOTS)
    manifest = {"status": "generated", "figure_count": 4, "files": FILES,
                "chart_data_path": data_path.relative_to(ROOT).as_posix(), "chart_values": len(DATA_FOR_PLOTS),
                "automatic_layout_checks": "Visible labels inside canvas; legends do not overlap title or subtitle. PNGs also require visual inspection.",
                "matplotlib_version": matplotlib.__version__, "numpy_version": np.__version__,
                "input_sha256": audit["analysis_csv_sha256"],
                "interpretation": "Descriptive figures from the validated 90-day analysis. No new strategy parameters or independently sampled events."}
    (ROOT / "reports/figures_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"figures": 4, "files": len(FILES), "chart_values": len(DATA_FOR_PLOTS), "output_directory": str(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
