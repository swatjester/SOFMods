#!/usr/bin/env python3
"""SOFMods validation: JSON parse, legacy item types, cross-references, sprite chains.

Usage: python3 tools/validate.py --tlg /path/to/Cataclysm-TLG/data/json

Builds an id universe from TLG base data + all mods in this repo, then checks:
- every file parses
- no legacy item types (AMMO/GUN/... must be ITEM + subtypes)
- copy-from, ammo/ammotype, magazines, item/ammo restrictions, ammo_effects,
  default/built-in mods, magazine adaptors, deploy-furniture, item groups,
  variants, professions (items/CBMs/traits/skills), scenarios (professions/locs),
  vehicles (parts incl. part#variant and auto turret_<gun>), vehicle groups
- looks_like sprite chains: every mod item must reach a TLG base item
  (copy-from implies looks_like ONLY if the target is already loaded, so
  prefer explicit looks_like pointing at a vanilla item with tileset art)
"""
import argparse, glob, json, os, sys
from collections import defaultdict

ITEM_TYPES = {'ITEM'}
LEGACY = {'AMMO','GUN','GUNMOD','MAGAZINE','ARMOR','TOOL','TOOL_ARMOR','COMESTIBLE',
          'BOOK','GENERIC','BIONIC_ITEM','PET_ARMOR','ENGINE','WHEEL','TOOLMOD','BATTERY'}
errors = []
def err(msg): errors.append(msg)

def load_all(root):
    objs = []
    for p in glob.glob(os.path.join(root, '**', '*.json'), recursive=True):
        try:
            with open(p, encoding='utf-8') as f: data = json.load(f)
        except Exception as e:
            err(f'PARSE: {p}: {e}'); continue
        if isinstance(data, dict): data = [data]
        for o in data:
            if isinstance(o, dict): o['_file'] = p; objs.append(o)
    return objs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tlg', required=True, help='path to TLG data/json')
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    base = load_all(args.tlg)
    mod = load_all(os.path.join(repo))
    mod = [o for o in mod if 'Modern_SOF' in o['_file']]

    ids = defaultdict(set)
    base_items, mod_items = set(), {}
    CAT = {'ammunition_type':'ammotype','ammo_effect':'ammo_effect','effect_type':'effect',
           'item_group':'group','profession':'profession','scenario':'scenario','vehicle':'vehicle',
           'vehicle_part':'vpart','vehicle_group':'vgroup','furniture':'furniture','bionic':'bionic',
           'start_location':'sloc','effect_on_condition':'eoc','MONSTER':'monster','monster':'monster',
           'skill':'skill','mutation':'trait','flag':'flag','json_flag':'flag','monstergroup':'mongroup'}
    for src, objs in (('base', base), ('mod', mod)):
        for o in objs:
            t = o.get('type'); i = o.get('id') or o.get('abstract')
            if not t or not isinstance(i, str): continue
            if t in ITEM_TYPES or t in LEGACY:
                ids['item'].add(i)
                ids['vpart'].add('turret_' + i)  # guns can back auto turret parts
                if src == 'base': base_items.add(i)
                else: mod_items[i] = o
                for blk in (o.get('variants') or []) + ((o.get('extend') or {}).get('variants') or []):
                    if isinstance(blk, dict) and blk.get('id'): ids['variant'].add(blk['id'])
            elif t in CAT: ids[CAT[t]].add(i)
            if t == 'snippet' and o.get('category'): ids['snippet'].add(o['category'])

    def item_ok(v): return isinstance(v, str) and (v in ids['item'] or v in ('NULL','null'))
    def ck_item(v, ctx, what='item'):
        if isinstance(v, str) and not item_ok(v): err(f'{ctx}: unknown {what} "{v}"')

    for o in mod:
        f = os.path.relpath(o['_file'], repo); t = o.get('type')
        oid = o.get('id') or o.get('abstract') or '?'; ctx = f'{f} [{t}:{oid}]'
        if t in LEGACY: err(f'{ctx}: legacy type "{t}" — use ITEM + subtypes'); continue
        cf = o.get('copy-from')
        if cf:
            cat = CAT.get(t, 'item')
            if cf not in ids[cat] and cf not in ids['item']: err(f'{ctx}: copy-from "{cf}" not found')
        if t == 'ITEM':
            a = o.get('ammo')
            for x in (a if isinstance(a, list) else [a] if a else []):
                if x not in ids['ammotype'] and x != 'NULL': err(f'{ctx}: ammo type "{x}" unknown')
            for pd in o.get('pocket_data') or []:
                for r in pd.get('item_restriction') or []: ck_item(r, ctx)
                for k in pd.get('ammo_restriction') or {}:
                    if k not in ids['ammotype']: err(f'{ctx}: ammo_restriction "{k}" unknown')
            for m in (o.get('default_mods') or []) + (o.get('built_in_mods') or []): ck_item(m, ctx, 'gunmod')
            for entry in (o.get('magazines') or []) + (o.get('magazine_adaptor') or []):
                if isinstance(entry, list) and len(entry) == 2:
                    at, ml = entry
                    if at not in ids['ammotype']: err(f'{ctx}: magazine ammotype "{at}" unknown')
                    for m in ml: ck_item(m, ctx, 'magazine')
            for ae in o.get('ammo_effects') or []:
                if ae not in ids['ammo_effect'] and ae not in ids['flag']: err(f'{ctx}: ammo_effect "{ae}" unknown')
            am = o.get('ammo_modifier')
            for x in (am if isinstance(am, list) else [am] if am else []):
                if x not in ids['ammotype']: err(f'{ctx}: ammo_modifier "{x}" unknown')
            for amod in o.get('add_mod') or []:
                if isinstance(amod, list): ck_item(amod[0], ctx, 'gunmod')
            ua = o.get('use_action')
            if isinstance(ua, dict) and ua.get('type') == 'deploy_furn' and ua.get('furn_type') not in ids['furniture']:
                err(f'{ctx}: deploy furniture "{ua.get("furn_type")}" unknown')
        elif t == 'ammunition_type':
            if o.get('default') and o['default'] not in ids['item']: err(f'{ctx}: default ammo "{o["default"]}" unknown')
        elif t == 'item_group':
            def walk(g):
                if not isinstance(g, dict): return
                for k in ('item', 'contents-item', 'ammo-item', 'container-item'):
                    v = g.get(k)
                    for x in (v if isinstance(v, list) else [v] if v else []):
                        if isinstance(x, str): ck_item(x, ctx)
                        elif isinstance(x, dict): walk(x)
                for k in ('group', 'contents-group'):
                    v = g.get(k)
                    for x in (v if isinstance(v, list) else [v] if v else []):
                        if isinstance(x, str) and x not in ids['group']: err(f'{ctx}: unknown group "{x}"')
                if g.get('variant') and g['variant'] not in ids['variant']: err(f'{ctx}: unknown variant "{g["variant"]}"')
                for k in ('entries', 'items', 'groups'):
                    for e in g.get(k) or []:
                        if isinstance(e, dict): walk(e)
                        elif isinstance(e, list) and e and isinstance(e[0], str):
                            if k == 'groups':
                                if e[0] not in ids['group']: err(f'{ctx}: unknown group "{e[0]}"')
                            else: ck_item(e[0], ctx)
                        elif isinstance(e, str):
                            if k == 'groups':
                                if e not in ids['group']: err(f'{ctx}: unknown group "{e}"')
                            else: ck_item(e, ctx)
            walk(o)
        elif t == 'profession':
            def walk_e(es):
                for e in es or []:
                    if isinstance(e, str): ck_item(e, ctx); continue
                    if not isinstance(e, dict): continue
                    if e.get('item'): ck_item(e['item'], ctx)
                    if e.get('group') and e['group'] not in ids['group']: err(f'{ctx}: unknown group "{e["group"]}"')
                    for k in ('ammo-item', 'container-item', 'contents-item'):
                        v = e.get(k)
                        for x in (v if isinstance(v, list) else [v] if v else []): ck_item(x, ctx)
                    for x in (lambda v: v if isinstance(v, list) else [v] if v else [])(e.get('contents-group')):
                        if x not in ids['group']: err(f'{ctx}: unknown contents-group "{x}"')
                    if e.get('variant') and e['variant'] not in ids['variant']: err(f'{ctx}: unknown variant "{e["variant"]}"')
            it = o.get('items') or {}
            for k in ('both', 'male', 'female'):
                v = it.get(k)
                walk_e(v.get('entries') if isinstance(v, dict) else v)
            for c in o.get('CBMs') or []:
                if c not in ids['bionic']: err(f'{ctx}: unknown CBM "{c}"')
            for s in o.get('skills') or []:
                if isinstance(s, dict) and s.get('name') not in ids['skill']: err(f'{ctx}: unknown skill "{s.get("name")}"')
            for tr in o.get('traits') or []:
                if tr not in ids['trait']: err(f'{ctx}: unknown trait "{tr}"')
        elif t == 'scenario':
            for p in o.get('professions') or []:
                if p not in ids['profession']: err(f'{ctx}: unknown profession "{p}"')
            for l in o.get('allowed_locs') or []:
                if l not in ids['sloc']: err(f'{ctx}: unknown start_location "{l}"')
        elif t == 'vehicle':
            for part in o.get('parts') or []:
                plist = part.get('parts') or ([part.get('part')] if part.get('part') else [])
                for p in plist:
                    pid = p if isinstance(p, str) else (p.get('part') if isinstance(p, dict) else None)
                    if pid and pid.split('#')[0] not in ids['vpart']: err(f'{ctx}: unknown vehicle part "{pid}"')
                    if isinstance(p, dict):
                        for at in p.get('ammo_types') or []:
                            if at not in ids['item'] and at not in ids['ammotype']: err(f'{ctx}: turret ammo "{at}" unknown')
            for it_ in o.get('items') or []:
                for nm in ('item_groups', 'items'):
                    v = it_.get(nm); v = [v] if isinstance(v, str) else v
                    for x in v or []:
                        if nm == 'item_groups':
                            if x not in ids['group']: err(f'{ctx}: unknown item_group "{x}"')
                        else: ck_item(x, ctx)
        elif t == 'vehicle_part':
            if o.get('item'): ck_item(o['item'], ctx)
            for b in o.get('breaks_into') if isinstance(o.get('breaks_into'), list) else []:
                if isinstance(b, dict) and b.get('item'): ck_item(b['item'], ctx)
        elif t == 'vehicle_group':
            for v in o.get('vehicles') or []:
                if isinstance(v, list) and v[0] not in ids['vehicle']: err(f'{ctx}: unknown vehicle "{v[0]}"')
        elif t == 'furniture':
            ea = o.get('examine_action')
            if isinstance(ea, dict) and ea.get('type') == 'mortar':
                for a in ea.get('ammo') or []:
                    if a not in ids['ammotype']: err(f'{ctx}: mortar ammo type "{a}" unknown')
            if o.get('deployed_item'): ck_item(o['deployed_item'], ctx)

    # sprite chains
    def reaches_base(iid, seen=None):
        seen = seen or set()
        if iid in seen: return False
        seen.add(iid)
        if iid in base_items: return True
        o = mod_items.get(iid)
        if not o: return False
        nxt = o.get('looks_like') or o.get('copy-from')
        return bool(nxt) and nxt != iid and reaches_base(nxt, seen)
    for iid, o in sorted(mod_items.items()):
        if o.get('copy-from') == iid: continue  # extending a base item in place
        if not reaches_base(iid):
            err(f'{os.path.relpath(o["_file"], repo)} [ITEM:{iid}]: looks_like chain never reaches a TLG base item (no sprite)')
        ll = o.get('looks_like')
        if ll and ll not in ids['item']: err(f'{os.path.relpath(o["_file"], repo)} [ITEM:{iid}]: looks_like "{ll}" unknown')

    if errors:
        print(f'{len(errors)} problem(s):'); [print(' -', e) for e in errors]; sys.exit(1)
    print('OK: all checks passed')

if __name__ == '__main__':
    main()
