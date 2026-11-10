"""Obsunięcie kapitału osobnych koszyków zdarzeń; bez łączenia sygnałów."""

import hashlib
import json
import statistics
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal as D

from analyze_trades import ROOT, read_csv, save_json, write_csv

BUDGET = D(1000)


def capital_path(group, prices, costs, budget=BUDGET):
    """Stała liczba jednostek, dzienne wyceny rynkowe i koszty faktycznych wejść/wyjść."""
    assert len(group) == 5 and len({r['asset_id'] for r in group}) == 5
    assert all(r['status'] == 'completed' for r in group)
    for key in ('event_id', 'entry_rule', 'entry_date', 'exit_date', 'holding_days'):
        assert len({r[key] for r in group}) == 1, key
    entry = date.fromisoformat(group[0]['entry_date'])
    exit_day = date.fromisoformat(group[0]['exit_date'])
    days = (exit_day - entry).days
    assert days == int(group[0]['holding_days']) == 90
    buy = (1 + D(str(costs['adverse_buy_slippage']))) * (1 + D(str(costs['buy_fee_rate'])))
    sell = (1 - D(str(costs['adverse_sell_slippage']))) * (1 - D(str(costs['sell_fee_rate'])))
    allocation = budget / 5
    quantities = {side: [allocation / (D(r[f'{side}_entry_open']) * buy) for r in group] for side in ('alt', 'btc')}

    def value(side, stage, day=None):
        result = D(0)
        for r, quantity in zip(group, quantities[side]):
            if stage in ('entry_mark', 'exit_cash'):
                price = D(r[f'{side}_{"entry" if stage == "entry_mark" else "exit"}_open'])
            else:
                asset = r['asset_id'] if side == 'alt' else 'bitcoin'
                price = D(prices[(asset, r['venue'], day.isoformat())]['close'])
            result += quantity * price
        return result * sell if stage == 'exit_cash' else result

    samples = [('initial_cash', entry, budget, budget),
               ('entry_mark', entry, value('alt', 'entry_mark'), value('btc', 'entry_mark'))]
    for offset in range(days):
        day = entry + timedelta(days=offset)
        samples.append(('daily_close', day, value('alt', 'daily_close', day), value('btc', 'daily_close', day)))
    samples.append(('exit_cash', exit_day, value('alt', 'exit_cash'), value('btc', 'exit_cash')))
    peaks = {'alt': budget, 'btc': budget}
    peak_indices = {'alt': 0, 'btc': 0}
    rows = []
    for index, (stage, day, alt, btc) in enumerate(samples):
        row = {'event_id': group[0]['event_id'], 'entry_rule': group[0]['entry_rule'],
               'observation_index': index, 'date_utc': day.isoformat(), 'stage': stage}
        for side, capital in (('alt', alt), ('btc', btc)):
            assert capital > 0
            if capital > peaks[side]:
                peaks[side], peak_indices[side] = capital, index
            row.update({f'{side}_capital_usdt': capital, f'{side}_running_peak_usdt': peaks[side],
                        f'{side}_drawdown': capital / peaks[side] - 1,
                        f'{side}_peak_observation_index': peak_indices[side]})
        rows.append(row)
    return rows


def risk_for_path(path, event):
    row = {key: event[key] for key in ('event_id', 'entry_rule', 'signal_date', 'entry_date', 'exit_date', 'holding_days', 'signal_period', 'symbols', 'btc_venue_weights')}
    row.update(initial_budget_usdt=BUDGET, observations=len(path))
    for side in ('alt', 'btc'):
        trough = min(path, key=lambda r: r[f'{side}_drawdown'])
        peak = path[trough[f'{side}_peak_observation_index']]
        final = path[-1][f'{side}_capital_usdt']
        expected = BUDGET * (1 + D(event[f'event_mean_{side}_net_return']))
        assert abs(final - expected) < D('1e-32'), (row['event_id'], side, final, expected)
        row.update({f'{side}_mdd': trough[f'{side}_drawdown'],
                    f'{side}_peak_date': peak['date_utc'], f'{side}_trough_date': trough['date_utc'],
                    f'{side}_peak_stage': peak['stage'], f'{side}_trough_stage': trough['stage'],
                    f'{side}_peak_capital_usdt': peak[f'{side}_capital_usdt'],
                    f'{side}_trough_capital_usdt': trough[f'{side}_capital_usdt'],
                    f'{side}_final_capital_usdt': final})
    row['alt_less_severe_mdd'] = row['alt_mdd'] > row['btc_mdd']
    return row


def summarize(rows):
    result = []
    for rule in ('A', 'B', 'C'):
        group = [r for r in rows if r['entry_rule'] == rule]
        row = {'entry_rule': rule, 'completed_events': len(group)}
        for side in ('alt', 'btc'):
            values = [r[f'{side}_mdd'] for r in group]
            worst = min(group, key=lambda r: r[f'{side}_mdd'])
            row.update({f'median_{side}_mdd': statistics.median(values),
                        f'mean_{side}_mdd': statistics.mean(values), f'worst_{side}_mdd': min(values),
                        f'worst_{side}_event_id': worst['event_id'],
                        f'worst_{side}_signal_date': worst['signal_date']})
        row['alt_less_severe_mdd_count'] = sum(r['alt_less_severe_mdd'] for r in group)
        result.append(row)
    return result


def main():
    original = json.loads((ROOT / 'reports/trade_output_validation.json').read_text(encoding='utf-8'))['analysis_csv_sha256']
    for relative, digest in original.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest
    prices = {(r['asset_id'], r['venue'], r['date_utc']): r for r in read_csv('data/processed/market_prices_daily.csv')}
    groups = defaultdict(list)
    for r in read_csv('data/analysis/trades_90d.csv'):
        groups[(r['event_id'], r['entry_rule'])].append(r)
    events = {(r['event_id'], r['entry_rule']): r for r in read_csv('data/analysis/event_mean_returns_90d.csv')}
    costs = json.loads((ROOT / 'config/trade_protocol_v1.json').read_text(encoding='utf-8'))['base_costs']
    paths, risks = [], []
    for key, group in sorted(groups.items()):
        path = capital_path(group, prices, costs)
        paths.extend(path)
        risks.append(risk_for_path(path, events[key]))
    assert len(risks) == 60 and len(paths) == 5580
    summary = summarize(risks)
    outputs = {'basket_capital_path_90d.csv': paths, 'basket_capital_risk_90d.csv': risks,
               'summary_basket_capital_risk_90d.csv': summary}
    for name, rows in outputs.items():
        write_csv('data/analysis/' + name, rows)
    save_json('reports/basket_capital_risk_90d.json', {
        'reporting_extension_defined_after_original_results': True,
        'initial_budget_usdt_per_event': BUDGET, 'separate_budget_per_signal': True,
        'initial_weights': '20% per asset including buy costs; fixed quantities; no rebalancing',
        'valuation': 'Initial cash; market value immediately after entry; 90 daily closes UTC; actual net exit cash. No hypothetical liquidation cost at each daily mark.',
        'benchmark': 'Five equally allocated, venue-matched BTC positions, same dates and costs.',
        'drawdown_sign': 'Negative ratio: capital / prior running peak - 1; MDD is minimum.',
        'scope': 'Per-event 90-day paths, not one capital-constrained 2020-2025 account; intraday drawdown not reconstructed.',
        'observations': len(paths), 'event_rule_paths': len(risks), 'original_analysis_csv_unchanged': len(original),
        'definition_source': 'https://www.quantconnect.com/docs/v2/cloud-platform/optimization/objectives',
        'input_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in ('data/processed/market_prices_daily.csv', 'data/analysis/trades_90d.csv', 'data/analysis/event_mean_returns_90d.csv', 'config/trade_protocol_v1.json')},
        'output_sha256': {name: hashlib.sha256((ROOT / 'data/analysis' / name).read_bytes()).hexdigest() for name in outputs},
        'summary': summary})
    print(json.dumps(summary, ensure_ascii=False, default=str, indent=2))


if __name__ == '__main__':
    main()
