"""Kontrole ekonomicznego znaczenia oraz niezależne odtworzenie 60 ścieżek."""

import csv
import json
import sys
import unittest
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from analyze_basket_drawdown import capital_path


def read(name):
    with (ROOT / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


class BasketDrawdownTests(unittest.TestCase):
    def synthetic(self, sequences, costs=None):
        costs = costs or dict(buy_fee_rate=0, sell_fee_rate=0, adverse_buy_slippage=0, adverse_sell_slippage=0)
        entry = date(2020, 1, 1)
        group, prices = [], {}
        for i in range(5):
            group.append(dict(event_id='test', entry_rule='A', entry_date='2020-01-01', exit_date='2020-03-31',
                              holding_days='90', asset_id=str(i), venue='test', status='completed',
                              alt_entry_open='100', btc_entry_open='100', alt_exit_open='100', btc_exit_open='100'))
            seq = sequences[i]
            for offset in range(90):
                day = (entry + timedelta(days=offset)).isoformat()
                prices[(str(i), 'test', day)] = {'close': str(seq[min(offset, len(seq)-1)])}
                prices[('bitcoin', 'test', day)] = {'close': '100'}
        return capital_path(group, prices, costs)

    def test_peak_to_trough_even_when_no_final_loss(self):
        path = self.synthetic([[100, 120, 90, 100]] * 5)
        self.assertEqual(min(r['alt_drawdown'] for r in path), D('-.25'))
        self.assertEqual(path[-1]['alt_capital_usdt'], D(1000))
        trough = min(path, key=lambda r: r['alt_drawdown'])
        self.assertEqual(path[trough['alt_peak_observation_index']]['date_utc'], '2020-01-02')

    def test_flat_prices_capture_only_actual_transaction_costs(self):
        costs = dict(buy_fee_rate=.001, sell_fee_rate=.001, adverse_buy_slippage=.0005, adverse_sell_slippage=.0005)
        path = self.synthetic([[100]] * 5, costs)
        expected = (D('.999') * D('.9995')) / (D('1.001') * D('1.0005')) - 1
        self.assertLess(abs(min(r['alt_drawdown'] for r in path) - expected), D('1e-37'))
        self.assertEqual(path[2]['alt_capital_usdt'], path[-2]['alt_capital_usdt'])
        self.assertEqual(len(path), 93)

    def test_basket_risk_is_not_average_of_individual_drawdowns(self):
        path = self.synthetic([[100, 120, 80, 100], [100, 80, 120, 100], [100], [100], [100]])
        self.assertEqual(min(r['alt_drawdown'] for r in path), D(0))
        self.assertTrue(all(r['alt_capital_usdt'] == 1000 for r in path))

    def test_all_saved_paths_independently_from_prices_and_cash_flows(self):
        prices = {(r['asset_id'], r['venue'], r['date_utc']): float(r['close']) for r in read('data/processed/market_prices_daily.csv')}
        groups, paths = defaultdict(list), defaultdict(list)
        for r in read('data/analysis/trades_90d.csv'):
            groups[(r['event_id'], r['entry_rule'])].append(r)
        for r in read('data/analysis/basket_capital_path_90d.csv'):
            paths[(r['event_id'], r['entry_rule'])].append(r)
        risks = {(r['event_id'], r['entry_rule']): r for r in read('data/analysis/basket_capital_risk_90d.csv')}
        events = {(r['event_id'], r['entry_rule']): r for r in read('data/analysis/event_mean_returns_90d.csv')}
        costs = json.loads((ROOT / 'config/trade_protocol_v1.json').read_text())['base_costs']
        buy = (1 + costs['buy_fee_rate']) * (1 + costs['adverse_buy_slippage'])
        sell = (1 - costs['sell_fee_rate']) * (1 - costs['adverse_sell_slippage'])
        self.assertEqual(len(groups), 60)
        for key, trades in groups.items():
            stored = paths[key]
            self.assertEqual(len(stored), 93)
            for side in ('alt', 'btc'):
                quantities = [200 / (float(r[f'{side}_entry_open']) * buy) for r in trades]
                entry = date.fromisoformat(trades[0]['entry_date'])
                values = [1000., 1000 / buy]
                for day_offset in range(90):
                    day = (entry + timedelta(days=day_offset)).isoformat()
                    values.append(sum(q * prices[(r['asset_id'] if side == 'alt' else 'bitcoin', r['venue'], day)] for q, r in zip(quantities, trades)))
                values.append(sum(q * float(r[f'{side}_exit_open']) * sell for q, r in zip(quantities, trades)))
                peak, drawdowns = 1000., []
                for value, row in zip(values, stored):
                    peak = max(peak, value)
                    dd = value / peak - 1
                    drawdowns.append(dd)
                    self.assertAlmostEqual(value, float(row[f'{side}_capital_usdt']), places=8)
                    self.assertAlmostEqual(dd, float(row[f'{side}_drawdown']), places=12)
                self.assertAlmostEqual(min(drawdowns), float(risks[key][f'{side}_mdd']), places=12)
                self.assertAlmostEqual(values[-1] / 1000 - 1, float(events[key][f'event_mean_{side}_net_return']), places=12)


if __name__ == '__main__':
    unittest.main()
