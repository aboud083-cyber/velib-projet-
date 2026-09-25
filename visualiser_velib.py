"""Créer un tableau consultable des vélos disponibles depuis l'export MongoDB."""
import json
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'VelibDB.velib_collection.json'
if not SOURCE.exists():
    SOURCE = BASE / 'upload' / 'VelibDB.velib_collection.json'
DEST = BASE / 'index.html'

raw = json.loads(SOURCE.read_text(encoding='utf-8'))
stations = []
for row in raw:
    geo = json.loads(row['coordonnees_geo'])
    stations.append({
        'name': row['name'],
        'commune': row['nom_arrondissement_communes'],
        'bikes': row['numbikesavailable'],
        'mechanical': row['mechanical'],
        'ebike': row['ebike'],
        'renting': row['is_renting'] == 'OUI',
        'lat': round(geo['lat'], 7),
        'lon': round(geo['lon'], 7),
    })

stations.sort(key=lambda x: (not x['renting'], -x['bikes'], x['name']))
def fr(n):
    return f'{n:,}'.replace(',', ' ')

rows = []
for x in stations:
    name, commune = escape(x['name']), escape(x['commune'])
    url = f"https://www.openstreetmap.org/?mlat={x['lat']}&mlon={x['lon']}#map=18/{x['lat']}/{x['lon']}"
    status = 'Location possible' if x['renting'] else 'Location indisponible'
    cls = '' if x['renting'] else ' class="closed"'
    rows.append(f'<tr data-search="{escape((x["name"]+" "+x["commune"]).casefold(), quote=True)}">'
                f'<td>{name}</td><td>{commune}</td><td class="num">{fr(x["bikes"])}</td>'
                f'<td class="num">{fr(x["mechanical"])}</td><td class="num">{fr(x["ebike"])}</td>'
                f'<td{cls}>{status}</td><td><a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">Carte</a></td></tr>')

template = r'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vélib’ — vélos disponibles par station</title>
<style>
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color:#162b30;background:#f4f8f8}
body{max-width:1130px;margin:0 auto;padding:24px}h1{font-size:1.7rem;margin:0 0 8px}p{line-height:1.5}
.muted{color:#54676b}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}.stat{background:#fff;border:1px solid #d8e3e4;border-radius:10px;padding:12px 18px;min-width:170px}.stat strong{display:block;font-size:1.5rem;color:#086d65}
label{display:block;font-weight:600;margin-bottom:5px}input{font:inherit;border:1px solid #a7b9bc;border-radius:8px;padding:11px;width:min(100%,550px);box-sizing:border-box;background:white}
.controls{display:flex;gap:16px;align-items:end;flex-wrap:wrap;margin:20px 0}.controls span{padding-bottom:11px}
.tablewrap{overflow-x:auto;background:white;border:1px solid #d8e3e4;border-radius:10px}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:11px 13px;border-bottom:1px solid #e6eeee}th{background:#e9f2f1;white-space:nowrap}td.num{text-align:right;font-variant-numeric:tabular-nums}.bar{height:7px;width:90px;border-radius:5px;background:#e0ebea;display:inline-block;margin-left:9px;vertical-align:middle}.bar i{display:block;background:#0c8175;height:100%;border-radius:5px}a{color:#066d73}tr:last-child td{border:0}.closed{color:#a34d3f;font-weight:600}.foot{font-size:.9rem;color:#54676b;margin-top:14px}
@media(max-width:700px){body{padding:14px}.bar{display:none}th,td{padding:9px 7px;font-size:.87rem}}
</style></head><body>
<h1>Vélos disponibles par station Vélib’</h1>
<p class="muted">Les chiffres reflètent l’export fourni, sans date de collecte fiable. Si la recherche ne réagit pas dans votre aperçu, ouvrez le fichier dans Chrome ou Edge, ou utilisez Ctrl+F.</p>
<div class="stats"><div class="stat"><strong>__COUNT__</strong>stations dans l’export</div><div class="stat"><strong>__RENT__</strong>stations ouvertes à la location</div><div class="stat"><strong>__BIKES__</strong>vélos dans les stations ouvertes</div></div>
<div class="controls"><div><label for="query">Rechercher une station ou une commune</label><input id="query" type="search" placeholder="Ex. Charcot, Romainville…"></div><span id="found" aria-live="polite"></span></div>
<div class="tablewrap"><table><thead><tr><th>Station (repère d’adresse)</th><th>Commune</th><th>Vélos disponibles</th><th>Classiques</th><th>Électriques</th><th>Situation</th><th>Localiser</th></tr></thead><tbody id="rows">__ROWS__</tbody></table></div>
<p class="foot">Le fichier ne contient aucune adresse postale ni numéro de rue : le nom de la station et sa commune servent de repère. « Localiser » ouvre ses coordonnées sur OpenStreetMap. Une station fermée à la location est signalée même si des vélos y sont comptés.</p>
<script>const input=document.getElementById('query'), items=[...document.querySelectorAll('#rows tr')], count=document.getElementById('found');
function render(){let q=input.value.trim().toLocaleLowerCase('fr'), shown=0;for(const row of items){let ok=row.dataset.search.includes(q);row.hidden=!ok;if(ok)shown++}count.textContent=shown.toLocaleString('fr-FR')+' station(s)'}
input.addEventListener('input',render);render();</script>
</body></html>'''
page = (template.replace('__ROWS__', '\n'.join(rows))
        .replace('__COUNT__', fr(len(stations)))
        .replace('__RENT__', fr(sum(x['renting'] for x in stations)))
        .replace('__BIKES__', fr(sum(x['bikes'] for x in stations if x['renting']))))
DEST.write_text(page, encoding='utf-8')
print(f'{len(stations)} stations -> {DEST} ({DEST.stat().st_size} bytes)')
