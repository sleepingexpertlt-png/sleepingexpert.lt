#!/usr/bin/env python3
"""Generate a Finvalda sales-import XML (fvsdata / pardavimas) from a sales register CSV.

Input CSV columns (as in the Google Sheets sales register):
  Menuo, Sask. data, Numeris, Klientas, Kli. valstybe, Zurn., Tipas, PVM %, Kliento PVM kodas,
  Suma be PVM, PVM, Viso suma, Uzsak. Nr. (is pastabos), WC uzsak. Nr., Uzsak. data, Vieta, Pastaba, ...

Rules (VPS: reference_finvalda_xml_format.md, lessons.md 2026-05-20):
  - dates YYYY-MM-DD, decimals with a dot, pretty-printed multi-line XML, UTF-8
  - LT sale: pvm_kodas PVM1, pvm_proc 21.00; EU reverse charge: PVM21, pvm_proc 0.00
  - invoice numbers only from the source (OSL serija + 6-digit dokumentas), never invented
  - line <kodas> = PAJAMOS for OSL sales (override with --kodas)
"""
import argparse, csv, re, unicodedata
from datetime import datetime
from xml.sax.saxutils import escape

def translit(s):
    s = unicodedata.normalize('NFKD', s)
    return ''.join(ch for ch in s if not unicodedata.combining(ch))

def client_code(name, country):
    m = re.search(r'\((?:k\.|NIP)\s*(\d+)\)', name)
    if 'Alina Group' in name: return 'ALINA'
    if m: return m.group(1)
    base = re.sub(r'[^A-Z0-9]', '', translit(name).upper())
    return base[:20] or 'KLIENTAS'

def clean_name(name):
    return re.sub(r'\s*\((?:k\.|NIP)\s*\d+\)', '', name).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv'); ap.add_argument('-o', '--out')
    ap.add_argument('--kodas', default='PAJAMOS', help='line <kodas> (PAJAMOS or 5001)')
    ap.add_argument('--sandelis', default='PAGR')
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.csv, encoding='utf-8-sig')))
    clients, ops = {}, []
    for r in rows:
        name = r['Klientas']; country = r['Kli. valstybe'] or 'LT'
        code = client_code(name, country)
        m = re.search(r'\((?:k\.|NIP)\s*(\d+)\)', name)
        eu = country != 'LT'
        clients.setdefault(code, dict(kodas=code, pavadinimas=clean_name(name), im_kodas=m.group(1) if m else '',
                                      pvm_kodas='PVM21' if eu else 'PVM1', salis_kodas=country))
        num = r['Numeris']; serija, dok = num[:3], num[3:]
        be, pvm, viso = (float(r[k]) for k in ('Suma be PVM', 'PVM', 'Viso suma'))
        assert abs(be + pvm - viso) < 0.011, num
        gid = r.get('Uzsak. Nr. (is pastabos)', '')
        pastaba = f"Užsak. Nr. {r['WC uzsak. Nr.']}"
        if gid and gid.isdigit(): pastaba += f"; gamintojo ID {gid}"
        if r.get('Pastaba', '').startswith('REVERSE'): pastaba += '; PVM įst. 13 str. 2 d., Dir. 2006/112/EB 44 str.'
        ops.append(dict(serija=serija, dok=dok, data=r['Sask. data'], klientas=code, pastaba=pastaba, num=num,
                        be=be, pvm=pvm, pvm_proc='0.00' if eu else '21.00', pvm_kodas='PVM21' if eu else 'PVM1',
                        pavadinimas=f"Pardavimas pagal sąskaitą {num} (WC {r['WC uzsak. Nr.']})"))
    L = ['<?xml version="1.0" encoding="utf-8" standalone="yes"?>', '<fvsdata>', '  <klientai>']
    for c in clients.values():
        L += ['    <klientas>'] + [f'      <{k}>{escape(str(v))}</{k}>' for k, v in c.items() if v != ''] + ['    </klientas>']
    L += ['  </klientai>', '  <prekes/>', '  <operacijos>']
    for o in ops:
        L += ['    <pardavimas>', '      <tipas>PARD</tipas>', '      <zurnalas>PARD</zurnalas>',
              f'      <serija>{o["serija"]}</serija>', f'      <dokumentas>{o["dok"]}</dokumentas>',
              f'      <data>{o["data"]}</data>', '      <valiuta>EUR</valiuta>',
              f'      <mokejimo_data>{o["data"]}</mokejimo_data>', f'      <reg_data>{o["data"]}</reg_data>',
              f'      <dokumento_data>{o["data"]}</dokumento_data>', f'      <klientas>{o["klientas"]}</klientas>',
              f'      <pastaba>{escape(o["pastaba"])}</pastaba>', f'      <pavadinimas1>{o["num"]}</pavadinimas1>',
              '      <imp_param>VA</imp_param>', '      <operacijaDet>', '        <eilute>',
              '          <tipas>2</tipas>', f'          <kodas>{a.kodas}</kodas>',
              '          <kiekis pirmas_mat="true">1.00</kiekis>', f'          <sandelis>{a.sandelis}</sandelis>',
              f'          <pavadinimas>{escape(o["pavadinimas"])}</pavadinimas>',
              f'          <suma_v>{o["be"]:.2f}</suma_v>', f'          <suma_l>{o["be"]:.2f}</suma_l>',
              f'          <suma_pvmv>{o["pvm"]:.2f}</suma_pvmv>', f'          <suma_pvml>{o["pvm"]:.2f}</suma_pvml>',
              f'          <pvm_proc>{o["pvm_proc"]}</pvm_proc>', f'          <pvm_kodas>{o["pvm_kodas"]}</pvm_kodas>',
              '        </eilute>', '      </operacijaDet>', '    </pardavimas>']
    L += ['  </operacijos>', '</fvsdata>', '']
    out = a.out or f"pardavimai_OSL_{ops[0]['num'][3:]}-{ops[-1]['num'][3:]}_{datetime.now():%Y-%m-%d_%H%M%S}.xml"
    open(out, 'w', encoding='utf-8').write('\n'.join(L))
    print(out, len(ops), 'pardavimai', len(clients), 'klientai', 'be PVM', round(sum(o['be'] for o in ops), 2), 'PVM', round(sum(o['pvm'] for o in ops), 2))

if __name__ == '__main__':
    main()
