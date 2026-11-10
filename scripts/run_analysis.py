"""Odtwarza analizę i sprawdza niezmienność opublikowanych wyników."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(*args):
    print('Uruchamianie: '+' '.join(args),flush=True)
    subprocess.run([sys.executable,*args],cwd=ROOT,check=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='Odtwórz również przygotowanie danych.')
    parser.add_argument('--figures',action='store_true',help='Eksportuj pięć wykresów PNG/SVG.')
    args=parser.parse_args()
    reference=json.loads((ROOT/'config/published_results_sha256.json').read_text(encoding='utf-8'))
    if args.full:
        for name in ('prepare_prices','build_signal_events','select_event_baskets','prepare_event_prices','check_ranking_source'):
            run('scripts/'+name+'.py')
    for name in ('analyze_trades','aggregate_event_results','validate_trade_outputs','analyze_basket_drawdown'):
        run('scripts/'+name+'.py')
    run('-m','unittest','discover','-s','tests','-p','test_*.py','-v')
    for name,digest in reference.items():
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual!=digest:raise RuntimeError('Wynik różni się od opublikowanej wersji: '+name)
    if args.figures:
        run('scripts/build_figures.py')
        run('scripts/build_drawdown_figure.py')
    print(f'Kontrola zakończona: {len(reference)} tabel wynikowych zgodnych z opublikowaną wersją.',flush=True)

if __name__=='__main__':main()
