"""Piąty wykres: mediana i najgłębsze obsunięcie kapitału osobnych koszyków."""

import hashlib
import json
from build_figures import ROOT, OUT, ALT, BTC, GRID, MUTED, plt, style, read_csv, percent_tick, pl


def main():
    rows = read_csv('data/analysis/summary_basket_capital_risk_90d.csv')
    style()
    fig, axes = plt.subplots(1, 2, figsize=(13, 7))
    fig.subplots_adjust(left=.14, right=.98, bottom=.25, top=.77, wspace=.42)
    fig.text(.07, .95, 'Maksymalne obsunięcie kapitału koszyka i BTC', fontsize=18, weight='bold', va='top')
    fig.text(.07, .89, '20 osobnych inwestycji na regułę · 90 dni · równe początkowe udziały pięciu monet', color=MUTED, fontsize=10.5)
    for ax, stat, title in zip(axes, ('median', 'worst'), ('Mediana MDD z 20 zdarzeń', 'Najgłębsze MDD w próbie')):
        for offset, side, color, label in ((-.18, 'alt', ALT, 'Koszyk altcoinów'), (.18, 'btc', BTC, 'Dopasowany BTC')):
            values = [float(r[f'{stat}_{side}_mdd']) * 100 for r in rows]
            bars = ax.barh([i + offset for i in range(3)], values, height=.30, color=color, label=label)
            for bar, value in zip(bars, values):
                ax.text(value - 1, bar.get_y()+bar.get_height()/2, pl(value, 2)+'%', ha='right', va='center', fontsize=10, color=color)
        ax.set_title(title, loc='left', pad=20)
        ax.set_yticks([0, 1, 2], ['A · D+1', 'B · D+7', 'C · powrót RSI'])
        ax.invert_yaxis()
        ax.set_xlim(-70, 0)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(percent_tick))
        ax.grid(axis='x', color=GRID, linewidth=.7)
        ax.set_axisbelow(True)
        ax.tick_params(length=0)
    axes[0].legend(loc='upper left', bbox_to_anchor=(0, -.16), ncol=2, fontsize=9)
    fig.text(.07, .12, 'MDD = najniższa wartość (kapitał / wcześniejsze maksimum − 1). Głębszy spadek oznacza większe ryzyko.\nWyceny: kapitał początkowy, wejście, dzienne zamknięcia i wpływ netto ze sprzedaży; modelowe koszty.\nNajgorsze zdarzenie może być inne dla koszyka i BTC. Nie jest to ścieżka jednego konta w latach 2020–2025.', color=MUTED, fontsize=9, linespacing=1.5, va='top')
    fig.text(.07, .025, 'Opracowanie własne · ceny: Binance / KuCoin · Data: CryptWatch, based on CoinMarketCap', fontsize=8, color=MUTED)
    files = []
    for extension in ('png', 'svg'):
        target = OUT / ('05_obsuniecie_kapitalu.' + extension)
        fig.savefig(target, dpi=220, metadata={'Creator': 'Mateusz Gromski'})
        files.append({'path': str(target.relative_to(ROOT)), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    plt.close(fig)
    (ROOT / 'reports/drawdown_figure_manifest.json').write_text(json.dumps({'files': files, 'source': 'data/analysis/summary_basket_capital_risk_90d.csv'}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(files))


if __name__ == '__main__':
    main()
