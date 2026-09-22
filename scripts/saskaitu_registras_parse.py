import re, json, csv
txt = open('saskaitos.txt', encoding='utf-8').read()
txt = re.sub(r'\n=== PAGE \d+\n', '\n', txt)
chunks = txt.split('PVM SĄSKAITA FAKTŪRA')[1:]

def after(label, s):
    m = re.search(re.escape(label) + r'\s*\n([^\n]+)', s)
    return m.group(1).strip() if m else ''

def num(s):
    return float(s.replace('.', '').replace(',', '.')) if s else 0.0

rows = []
for c in chunks:
    r = {}
    r['saskaitos_nr'] = after('Sąskaita Numeris:', c)
    r['saskaitos_data'] = after('Sąskaita Data:', c)
    r['uzsakymo_nr'] = after('Užsakymo numeris:', c)
    r['uzsakymo_data'] = after('Užsakymo data:', c)
    buyer = c.split('Siųsti į:')[0].strip().split('\n')
    r['pirkejas'] = buyer[0].strip()
    bb = '\n'.join(buyer)
    m = re.search(r'(?:įm\.?\s*k\.?|Kodas:|NIP)\s*\n?\s*(\d{8,11})', bb)
    r['imones_kodas'] = m.group(1) if m else ''
    if 'NIP' in bb and not r['imones_kodas']:
        m = re.search(r'NIP\s*\n?\s*(\d+)', c); r['imones_kodas'] = m.group(1) if m else ''
    # payment
    pm = re.search(r'Mokėjimo metodas:\s*\n(.*?)\nProduktas', c, re.S)
    r['mokejimo_metodas'] = re.sub(r'[^\w\s\-–|!]', '', pm.group(1).replace('\n', ' ')).strip() if pm else ''
    v = re.search(r'Vieta: ([^\n]+)', c); r['vieta'] = v.group(1).strip(' ,') if v else 'E-shop'
    mb = re.search(r'Mokėjimo būdas: ([^\n]+)', c); r['mokejimo_budas'] = mb.group(1).strip() if mb else ''
    av = re.search(r'Sumokėtas avansas: ([^\n]+)', c); r['avansas'] = av.group(1).strip() if av else ''
    lk = re.search(r'Likusi suma: ([^\n]+)', c); r['likusi_suma'] = lk.group(1).strip() if lk else ''
    # manufacturer ID from Pastaba region
    past = re.search(r'Pastaba:\s*\n(.*?)\nSuma\n', c, re.S)
    past_txt = past.group(1) if past else ''
    ids = sorted(set(re.findall(r'(?<!\d)(5\d{4})(?!\d)', past_txt)))
    r['gamintojo_id'] = ', '.join(ids) if ids else 'TRŪKSTA ID'
    r['pastaba'] = ' | '.join(l.strip() for l in past_txt.split('\n') if l.strip() and not l.startswith(('Darbuotojas','Vieta:','Mokėjimo būdas','Sumokėtas','Likusi','Papildomos')) and 'Parduotuvės užsakymas' not in l)
    # products
    prod = re.search(r'Kaina\n(.*?)\n(?:Pastaba:|Pirkėjo pastaba:|Suma\n)', c, re.S)
    names = []
    if prod:
        lines = prod.group(1).split('\n')
        for i, l in enumerate(lines):
            if l.startswith('Produkto kodas:') and i > 0:
                names.append(f"{lines[i-1].strip()} [{l.split(':',1)[1].strip()}]")
    r['prekes'] = '; '.join(names)
    viso = re.search(r'Viso\n([\d\.,]+) €', c); r['suma_su_pvm'] = num(viso.group(1)) if viso else 0
    pvm = re.search(r'įskaičiuota\s*([\d\.,]+)\s*€\s*PVM', c); r['pvm'] = num(pvm.group(1)) if pvm else 0.0
    r['suma_be_pvm'] = round(r['suma_su_pvm'] - r['pvm'], 2)
    r['pvm_tarifas'] = '21%' if r['pvm'] > 0 else '0%'
    nuol = re.search(r'Nuolaida\n-?([\d\.,]+) €', c); r['nuolaida'] = num(nuol.group(1)) if nuol else 0.0
    pr = re.search(r'Pristatymas\n([\d\.,]+) €', c); r['pristatymas'] = num(pr.group(1)) if pr else 0.0
    rows.append(r)

# CSV cross-check
csv_orders = {}
with open('/root/.claude/uploads/60843650-ac2d-52f2-a915-4dd49570e2f8/7bf94fe5-orders-2026-09-22-19-04-35.csv', encoding='utf-8-sig') as f:
    for d in csv.DictReader(f):
        csv_orders[d['Order Number']] = d
for r in rows:
    d = csv_orders.get(r['uzsakymo_nr'])
    if d:
        r['csv_total'] = float(d['Order Total Amount']); r['csv_tax'] = float(d['Order Total Tax Amount'])
        r['csv_email'] = d['Email (Billing)']; r['csv_status'] = d['Order Status']
        r['sutampa_su_csv'] = 'TAIP' if abs(r['csv_total'] - r['suma_su_pvm']) < 0.01 and abs(r['csv_tax'] - r['pvm']) < 0.01 else f"NE (CSV {r['csv_total']:.2f}/{r['csv_tax']:.2f})"
    else:
        r['csv_total'] = r['csv_tax'] = None; r['csv_email'] = r['csv_status'] = ''; r['sutampa_su_csv'] = 'NĖRA CSV'
json.dump(rows, open('register.json', 'w'), ensure_ascii=False, indent=1)
print(len(rows), 'invoices;', len(csv_orders), 'csv orders')
for r in rows:
    print(f"{r['saskaitos_nr']} {r['saskaitos_data']} | WC {r['uzsakymo_nr']} {r['uzsakymo_data']} | ID {r['gamintojo_id']:<14} | {r['pirkejas'][:28]:<28} | {r['vieta'][:12]:<12} | {r['suma_su_pvm']:>8.2f} pvm {r['pvm']:>7.2f} | {r['sutampa_su_csv']}")
missing_csv = set(csv_orders) - {r['uzsakymo_nr'] for r in rows}
print('CSV orders without invoice in PDF:', sorted(missing_csv))
