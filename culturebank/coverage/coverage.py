import sys
import io
from itertools import groupby
import json
from collections import Counter, defaultdict


def read(n):
    with io.open('%s.csv' % n, encoding='utf8') as fp:
        for i, line in enumerate(fp):
            yield [None if col == '[NULL]' else col for col in line.strip().split('+++')]


def _desctype(jd):
    if jd:
        jd = json.loads(jd)
        if jd and 'med' in jd and jd['med']:
            dt = jd['med']['doctype']
            if dt in ['grammar', 'grammarsketch']:
                return dt


def get_md(name, langs, mas):
    res = dict(name=name, extension=[], macroareas=set(), doctype=None, subgroups={})
    for lid, lname, ssfid, ssfname, sfid, sfname, fid, fname, jd in langs:
        if res['doctype'] != 'grammar':
            desctype = _desctype(jd)
            if desctype:
                res['doctype'] = desctype
        if mas.get(lid):
            res['macroareas'].add(mas[lid])
        res['extension'].append(lid)
    res['macroareas'] = list(res['macroareas'])
    return res


if __name__ == '__main__':
    macroareas = {r[0]: (r[1], r[2]) for r in read('macroareas')}

    res = {}
    log = Counter()

    # 0    1      2      3        4     5       6    7      8
    #lid, lname, ssfid, ssfname, sfid, sfname, fid, fname, jd
    for (fid, fname), langs in groupby(read('languages'), lambda r: (r[6], r[7])):
        langs = list(langs)        
        if fid:
            if fname in 'Bookkeeping|Mixed Language|Pidgin|Sign Language|Unclassifiable|Artificial Language'.split('|'):
                continue
            d = get_md(fname, langs, macroareas)
            if not d['doctype']:  # ignore everything that doesn't have a grammar or grammarsketch
                continue
            log.update(['family'])
            res[fid] = d

            for (sfid, sfname), slangs in groupby(langs, lambda r: (r[4], r[5])):
                slangs = list(slangs)
                if sfid:
                    dd = get_md(sfname, slangs, macroareas)
                    if not dd['doctype']:
                        continue
                    log.update(['subunit'])
                    res[fid]['subgroups'][sfid] = dd
                    for (ssfid, ssfname), sslangs in groupby(slangs, lambda r: (r[2], r[3])):
                        sslangs = list(sslangs)
                        if ssfid:
                            ddd = get_md(ssfname, sslangs, macroareas)
                            if ddd['doctype']:
                                 log.update(['subsubunit'])
                                 res[fid]['subgroups'][sfid]['subgroups'][ssfid] = ddd
        else:
            # isolates:
            for lid, lname, ssfid, ssfname, sfid, sfname, fid, fname, jd in langs:
                desctype = _desctype(jd)
                if desctype:
                    log.update(['isolate'])
                    res[lid] = {
                        'name': lname,
                        'doctype': desctype,
                        'macroareas': [macroareas[lid]],
                        'extension': [lid],
                    }

    with open('stats_by_classification.json', 'wb') as fp:
        json.dump(res, fp)


    stats = defaultdict(lambda: defaultdict(list))
    for fid, f in list(res.items()):
        for maname, maid in f['macroareas']:
            stats[maid][f['doctype']].append(fid)
    
    with open('stats_by_macroarea.json', 'wb') as fp:
        json.dump(stats, fp)

    macroareas = {r[1]: r[0] for r in set(macroareas.values())}
    with open('stats_macroareas.json', 'wb') as fp:
        json.dump(macroareas, fp)

    print(log)
    sys.exit(0)
