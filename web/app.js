(() => {
  const buttons = [...document.querySelectorAll('[data-rule]')];
  const level = document.getElementById('poziom');
  if (!level) return;
  let rule = 'A';
  let data;
  let lower = 0, upper = .06;
  const percentage = new Intl.NumberFormat('pl-PL',{style:'percent',minimumFractionDigits:2,maximumFractionDigits:2});
  const descriptions = {A:'A: zakup na otwarciu D+1, następnego dnia po świecy sygnałowej.',B:'B: zakup na otwarciu D+7 od daty świecy sygnałowej, sześć dni po wejściu A.',C:'C: zakup na kolejnym otwarciu po pierwszym powrocie RSI do co najmniej 30 w dniach D+1–D+30.'};
  function update() {
    if (!data) return;
    const basket = level.value === 'koszyki';
    const row = data[level.value][rule];
    const alt = Number(row[basket?'median_event_mean_alt_net_return':'median_alt_net_return']);
    const btc = Number(row[basket?'median_event_mean_btc_net_return':'median_btc_net_return']);
    const n = basket ? Number(row.completed_events) : Number(row.completed_trades);
    const scale = upper-lower;
    document.getElementById('alt-series').textContent = basket?'Koszyk pięciu monet':'Pojedyncze altcoiny';
    document.getElementById('alt-value').textContent = percentage.format(alt);
    document.getElementById('btc-value').textContent = percentage.format(btc);
    for (const [id,value] of [['alt-bar',alt],['btc-bar',btc]]) {
      const bar=document.getElementById(id);
      bar.style.width=`${Math.abs(value)/scale*100}%`;
      bar.style.left=`${(Math.min(0,value)-lower)/scale*100}%`;
    }
    document.getElementById('profit').textContent = `${row.success_profit_count}/${n}`;
    document.getElementById('advantage').textContent = `${row.success_btc_count}/${n}`;
    document.getElementById('sample').textContent = basket?`${n} koszyków z ${row.qualified_events} sygnałów; początkowo po 20% kapitału na monetę. Każdy sygnał ma odrębny budżet.`:`${n} par altcoin–BTC z ${row.qualified_events} sygnałów. Wyniki monet i nakładających się inwestycji są powiązane.`;
    document.getElementById('bar-pair').setAttribute('aria-label',`Mediana stóp zwrotu netto: ${basket?'koszyk':'altcoiny'} ${percentage.format(alt)}, BTC ${percentage.format(btc)}. Wspólna skala od ${percentage.format(lower)} do ${percentage.format(upper)}.`);
    document.getElementById('rule-description').textContent = descriptions[rule];
    buttons.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.rule === rule)));
  }
  buttons.forEach(button=>button.addEventListener('click',()=>{rule=button.dataset.rule;update();}));
  level.addEventListener('change',update);
  fetch('wyniki.json').then(response=>{if(!response.ok)throw new Error('data');return response.json();}).then(result=>{
    data=result;
    const all=Object.entries(data).flatMap(([key,rules])=>Object.values(rules).flatMap(r=>[Number(r[key==='koszyki'?'median_event_mean_alt_net_return':'median_alt_net_return']),Number(r[key==='koszyki'?'median_event_mean_btc_net_return':'median_btc_net_return'])]));
    if(all.length!==12||all.some(v=>!Number.isFinite(v)))throw new Error('data');
    lower=Math.min(0,Math.floor(Math.min(...all)/.02)*.02);
    upper=Math.max(.02,Math.ceil(Math.max(...all)/.02)*.02);
    const zero=(0-lower)/(upper-lower)*100;
    document.getElementById('bar-pair').style.setProperty('--comparison-zero',`${zero}%`);
    for(const [id,value] of [['scale-min',lower],['scale-middle',(lower+upper)/2],['scale-max',upper]])document.getElementById(id).textContent=percentage.format(value);
    update();
  }).catch(()=>{document.getElementById('rule-description').textContent='Nie udało się wczytać porównania. Odśwież stronę lub przejdź do pełnego raportu.';level.disabled=true;buttons.forEach(button=>button.disabled=true);});
})();

(() => {
  const eventSelect = document.getElementById('risk-event');
  if (!eventSelect) return;
  const ruleSelect = document.getElementById('risk-rule');
  const status = document.getElementById('risk-status');
  const figure = document.getElementById('risk-figure');
  const chart = document.getElementById('risk-chart');
  const values = document.getElementById('risk-values');
  const percentage = new Intl.NumberFormat('pl-PL',{style:'percent',minimumFractionDigits:2,maximumFractionDigits:2});
  const number = new Intl.NumberFormat('pl-PL',{maximumFractionDigits:1});
  let data;
  function update() {
    if (!data) return;
    const event = data.events.find(r=>r.event_id===eventSelect.value && r.entry_rule===ruleSelect.value);
    const path = data.paths.filter(r=>r.event_id===eventSelect.value && r.entry_rule===ruleSelect.value);
    if (!event || path.length!==93) throw new Error('Niekompletna ścieżka');
    const alt = Number(event.alt_mdd), btc = Number(event.btc_mdd);
    document.getElementById('risk-alt').textContent = percentage.format(alt);
    document.getElementById('risk-btc').textContent = percentage.format(btc);
    status.textContent = `Sygnał: ${event.signal_date}. Wejście: ${event.entry_date}, sprzedaż: ${event.exit_date}. Skład: ${event.symbols.split('|').join(', ')}. Daty UTC.`;
    figure.hidden = false;
    values.hidden = false;
    const width = Math.max(300,Math.min(900,Math.round(figure.getBoundingClientRect().width)));
    const height = width<500?290:330, left=55, right=16, top=20, bottom=48;
    const floor = -Math.max(.1,Math.ceil(Math.abs(Math.min(...path.flatMap(r=>[Number(r.alt_drawdown),Number(r.btc_drawdown)])))*10)/10);
    const x = day => left+day/90*(width-left-right);
    const y = value => top+value/floor*(height-top-bottom);
    const title = `Obsunięcie kapitału: sygnał ${event.signal_date}, reguła ${event.entry_rule}`;
    const description = `Maksymalne obsunięcie koszyka ${percentage.format(alt)}, dopasowanego BTC ${percentage.format(btc)}. Osobna inwestycja 90-dniowa.`;
    let svg = `<title id="risk-chart-title">${title}</title><desc id="risk-chart-description">${description}</desc>`;
    for(let i=0;i<=4;i++) {
      const value=i===0?0:floor*i/4;
      svg+=`<line x1="${left}" y1="${y(value)}" x2="${width-right}" y2="${y(value)}" stroke="#d4dce0"/><text x="${left-9}" y="${y(value)+4}" text-anchor="end" fill="#536572" font-size="12">${number.format(value*100)}%</text>`;
    }
    for(const day of [0,30,60,90]) svg+=`<text x="${x(day)}" y="${height-bottom+24}" text-anchor="middle" fill="#536572" font-size="12">${day}</text>`;
    svg+=`<text x="${width/2}" y="${height-3}" text-anchor="middle" fill="#536572" font-size="12">Dni od wejścia</text>`;
    for(const [side,color,dash] of [['alt','#166c88',''],['btc','#b46523','7 5']]) {
      const points=path.map((r,i)=>`${x(i<2?0:Math.min(90,i-1)).toFixed(2)},${y(Number(r[side+'_drawdown'])).toFixed(2)}`).join(' ');
      svg+=`<polyline points="${points}" fill="none" stroke="${color}" stroke-width="2.5" stroke-dasharray="${dash}" stroke-linejoin="round"/>`;
    }
    chart.setAttribute('viewBox',`0 0 ${width} ${height}`);
    chart.innerHTML=svg;
  }
  eventSelect.addEventListener('change',update);
  ruleSelect.addEventListener('change',update);
  new ResizeObserver(()=>{if(data)update();}).observe(figure);
  fetch('obsuniecie.json').then(r=>{if(!r.ok)throw new Error('data');return r.json();}).then(result=>{
    if(result.events.length!==60 || result.paths.length!==5580)throw new Error('data');
    data=result;
    eventSelect.replaceChildren();
    for(const event of data.events.filter(r=>r.entry_rule==='A')) {
      const option=document.createElement('option');option.value=event.event_id;option.textContent=event.signal_date;eventSelect.append(option);
    }
    eventSelect.disabled=false;ruleSelect.disabled=false;update();
  }).catch(()=>{
    data=null;eventSelect.disabled=true;ruleSelect.disabled=true;figure.hidden=true;values.hidden=true;
    status.textContent='Nie udało się wczytać ścieżek obsunięcia. Odśwież stronę lub przeczytaj pełne wyniki w raporcie.';
  });
})();
