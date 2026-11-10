"""Buduje przenośną stronę projektu z opublikowanych materiałów."""
import csv
import html
import json
import re
import shutil
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"_site"

def inline(value, pdf=False):
    value = html.escape(value)
    value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", lambda m: f'<{"link" if pdf else "a"} href="{m[2]}">{m[1]}</{"link" if pdf else "a"}>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return value

def blocks(value):
    lines = value.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == "---":
            i += 1
            continue
        if line.startswith("~~~") or line.startswith("```"):
            rows = []
            i += 1
            while i < len(lines) and not lines[i].startswith(("~~~", "```")):
                rows.append(lines[i])
                i += 1
            yield "code", rows
            i += 1
            continue
        if line.startswith("#"):
            m = re.match(r"(#+)\s+(.+)", line)
            yield "heading", (len(m[1]), m[2])
            i += 1
            continue
        if line.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(<?([^)>]+)>?\)", line)
            assert m, line
            yield "image", (m[1], m[2])
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", cell) for cell in row):
                    rows.append(row)
                i += 1
            yield "table", rows
            continue
        if line.startswith("- ") or re.match(r"\d+\. ", line):
            yield "item", re.sub(r"^(?:- |\d+\. )", "", line)
            i += 1
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(("#", "|", "![", "- ", "~~~", "```")):
            paragraph.append(lines[i].strip())
            i += 1
        yield "paragraph", " ".join(paragraph)

def article_html(markdown):
    output = []
    headings = []
    count = 0
    for kind, value in blocks(markdown):
        if kind == "heading":
            level, title = value
            count += 1
            identifier = "sekcja-" + str(count)
            level = 1 if count == 1 else min(level + 1, 4)
            if title.startswith(tuple(str(i) + "." for i in range(1,7))) or title == "Streszczenie":
                headings.append((identifier, title))
            output.append(f'<h{level} id="{identifier}">{inline(title)}</h{level}>')
        elif kind == "paragraph":
            output.append(f'<p>{inline(value)}</p>')
        elif kind == "item":
            output.append(f'<p class="list-item">{inline(value)}</p>')
        elif kind == "code":
            output.append('<pre><code>' + html.escape("\n".join(value)) + '</code></pre>')
        elif kind == "image":
            output.append(f'<figure><img src="raport/{html.escape(value[1])}" alt="{html.escape(value[0])}" loading="lazy"></figure>')
        elif kind == "table":
            output.append('<div class="table-scroll" tabindex="0" role="region" aria-label="Tabela wyników"><table><thead><tr>' + ''.join('<th scope="col">'+inline(c)+'</th>' for c in value[0]) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in value[1:]) + '</tbody></table></div>')
    return "\n".join(output), headings

def page(title,body):
    return f'''<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — Mateusz Gromski</title><meta name="description" content="Studium przypadku Google Data Analytics: historyczne wyniki pięciu altcoinów wobec BTC po sygnałach wyprzedania w latach 2020–2025."><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Przejdź do treści</a><header class="site-header"><a class="wordmark" href="index.html">Mateusz Gromski<span>Analiza danych</span></a><nav aria-label="Nawigacja główna"><a href="raport.html">Raport</a><a href="prezentacja.html">Prezentacja</a><a href="tableau.html">Tableau</a><a href="index.html#materialy">Materiały</a><a href="https://github.com/madridista011/altcoiny-btc-rsi-2020-2025">GitHub</a></nav></header><main id="main">{body}</main><footer><p>Mateusz Gromski · Studium przypadku Google Data Analytics · listopad 2026 r.</p><p>Ceny: Binance Spot / Binance Vision i KuCoin.<br>Data: CryptWatch, based on CoinMarketCap.</p></footer></body></html>'''

def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)

def main():
    SITE.mkdir(parents=True,exist_ok=True)
    for folder in ('raport','prezentacja','tableau','data/analysis','docs'):
        for path in (ROOT/folder).rglob('*'):
            if path.is_file():copy(path,SITE/path.relative_to(ROOT))
    report,headings=article_html((ROOT/'raport/RAPORT.md').read_text(encoding='utf-8'))
    navigation=''.join(f'<a href="#{identifier}">{html.escape(title)}</a>' for identifier,title in headings)
    report_body=f'<div class="report-heading"><a href="index.html">Powrót do projektu</a><a class="button" href="raport/RAPORT.pdf" download>Pobierz PDF</a></div><div class="report-layout"><aside class="contents"><h2>Spis treści</h2>{navigation}</aside><article class="report">{report}</article></div>'
    (SITE/'raport.html').write_text(page('Raport',report_body),encoding='utf-8')
    instruction,_=article_html((ROOT/'tableau/INSTRUKCJA.md').read_text(encoding='utf-8'))
    (SITE/'tableau.html').write_text(page('Dashboardy Tableau',f'<div class="report-heading"><a href="index.html">Powrót do projektu</a><a class="button" href="tableau/Altcoiny_RSI_BTC.twbx" download>Pobierz plik Tableau</a></div><article class="report instruction">{instruction}</article>'),encoding='utf-8')
    (SITE/'index.html').write_text(page('Altcoiny po wyprzedaniu BTC',(ROOT/'web/home.html').read_text(encoding='utf-8')),encoding='utf-8')
    slides='<div class="report-heading"><a href="index.html">Powrót do projektu</a><a class="button" href="prezentacja/Prezentacja.pptx" download>Pobierz prezentację PPTX</a></div><section class="slides"><h1>Prezentacja projektu</h1><p>Osiem slajdów podsumowujących cel, metodę, wyniki i ograniczenia badania.</p>'
    slides+=''.join(f'<figure><img src="prezentacja/slajdy/slajd-{i}.png" alt="Slajd {i} z 8" loading="lazy"><figcaption>Slajd {i} z 8</figcaption></figure>' for i in range(1,9))+'</section>'
    (SITE/'prezentacja.html').write_text(page('Prezentacja',slides),encoding='utf-8')
    for name in ('style.css','app.js'):copy(ROOT/'web'/name,SITE/name)
    summary={}
    for filename,key in (('summary_by_rule_90d.csv','monety'),('summary_event_means_90d.csv','koszyki')):
        with (ROOT/'data/analysis'/filename).open(encoding='utf-8-sig',newline='') as stream:
            summary[key]={r['entry_rule']:r for r in csv.DictReader(stream)}
    (SITE/'wyniki.json').write_text(json.dumps(summary,ensure_ascii=False),encoding='utf-8')
    risk={}
    for filename,key in (('summary_basket_capital_risk_90d.csv','summary'),('basket_capital_risk_90d.csv','events'),('basket_capital_path_90d.csv','paths')):
        with (ROOT/'data/analysis'/filename).open(encoding='utf-8-sig',newline='') as stream:
            risk[key]=list(csv.DictReader(stream))
        if key=='paths':risk[key]=[{**{k:r[k] for k in ('event_id','entry_rule')},**{k:round(float(r[k]),12) for k in ('alt_drawdown','btc_drawdown')}} for r in risk[key]]
    (SITE/'obsuniecie.json').write_text(json.dumps(risk,ensure_ascii=False),encoding='utf-8')
    folders=('config','data','docs','scripts','tests','raport','prezentacja','tableau','web','reports','assets','.github')
    files=[p for folder in folders for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    files.extend(p for p in ROOT.iterdir() if p.is_file() and (p.suffix in ('.md','.txt') or p.name in ('.gitignore','.gitattributes')))
    with ZipFile(SITE/'Altcoiny_BTC_Mateusz_Gromski.zip','w',ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            archive.write(path,'Altcoiny_BTC/'+path.relative_to(ROOT).as_posix())
    (SITE/'.nojekyll').touch()
    print(json.dumps({'site':'_site','files':sum(p.is_file() for p in SITE.rglob('*'))},ensure_ascii=False))

if __name__=='__main__':main()
