from collections import defaultdict, Counter, OrderedDict

from sqlalchemy import select
from pyramid.asset import abspath_from_asset_spec

from clldutils.jsonlib import load as jsonload
from clld.db.models.common import Language
from clld_glottologfamily_plugin.models import Family
from clld.db.meta import DBSession


#def about(req):
#    return {'data': req, 'map': IsoGlossMap(None, req)}

#@view_config(route_name='stability', renderer='stability.mako')
def stability(req):
    fs = jsonload(abspath_from_asset_spec('culturebank:static/stability.json'))
    #lfv = DBSession.query(Value).join(Value.valueset)\
    #        .options(
    #        joinedload(Value.valueset, ValueSet.language),
    #        joinedload(Value.valueset, ValueSet.parameter)
    #    )

    #trp = [(v.id,) for v in lfv]
    #sorted(fs.items(), key = lambda (f, s): s, reverse=True)
    return {'data': fs}

def dependencys(req):
    print("ANAL")
    deps = jsonload(abspath_from_asset_spec('culturebank:static/dependencies.json'))
    #lfv = DBSession.query(Value).join(Value.valueset)\
    #        .options(
    #        joinedload(Value.valueset, ValueSet.language),
    #        joinedload(Value.valueset, ValueSet.parameter)
    #    )

    #trp = [(v.id,) for v in lfv]
    #sorted(fs.items(), key = lambda (f, s): s, reverse=True)
    return {'data': deps}

def dependencies(req):
    print("HEJ")
    deps = jsonload(abspath_from_asset_spec('culturebank:static/dependencies.json'))
    #lfv = DBSession.query(Value).join(Value.valueset)\
    #        .options(
    #        joinedload(Value.valueset, ValueSet.language),
    #        joinedload(Value.valueset, ValueSet.parameter)
    #    )

    #trp = [(v.id,) for v in lfv]
    #sorted(fs.items(), key = lambda (f, s): s, reverse=True)
    return {'data': deps}

def dependency(req):
    print("HEJ2")
    deps = jsonload(abspath_from_asset_spec('culturebank:static/dependencies.json'))
    #lfv = DBSession.query(Value).join(Value.valueset)\
    #        .options(
    #        joinedload(Value.valueset, ValueSet.language),
    #        joinedload(Value.valueset, ValueSet.parameter)
    #    )

    #trp = [(v.id,) for v in lfv]
    #sorted(fs.items(), key = lambda (f, s): s, reverse=True)
    return {'data': deps}



def coverage(req):
    gl = jsonload(abspath_from_asset_spec('culturebank:static/stats_by_macroarea.json'))

    stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for ma in gl:
        for dt in gl[ma]:
            ids = gl[ma][dt]

            isolates = select(
                [Language.__table__.c.id]).where(Language.__table__.c.id.in_(ids))
            families = select(
                [Family.__table__.c.id]).where(Family.__table__.c.id.in_(ids))
            stats[ma][dt] = dict(
                glottolog=len(ids),
                culturebank=DBSession.query(isolates.union(families).alias('u')).count())
        stats[ma]['total'] = {}
        for src in ['glottolog', 'culturebank']:
            stats[ma]['total'][src] = \
                stats[ma]['grammar'][src] + stats[ma]['grammarsketch'][src]

    gl = jsonload(abspath_from_asset_spec('culturebank:static/stats_by_classification.json'))
    gb_langs = set([r[0] for r in DBSession.query(Language.id)])

    cstats = OrderedDict()
    for fid, spec in sorted(list(gl.items()), key=lambda k: k[1]['name']):
        d = dict(
            macroareas=spec['macroareas'],
            grammar=Counter(),
            grammarsketch=Counter(),
            total=Counter(),
            covered=gb_langs.intersection(set(spec['extension'])),
            isolate=not bool(spec.get('subgroups')),
            subgroups={})
        if not spec.get('subgroups'):
            # an isolate!
            d[spec['doctype']].update(['glottolog'])
            d['total'].update(['glottolog'])
            if gb_langs.intersection(set(spec['extension'])):
                d[spec['doctype']].update(['culturebank'])
                d['total'].update(['culturebank'])
        for sfid, sub in list(spec.get('subgroups', {}).items()):
            if not sub.get('subgroups'):
                sub['name'] = '%s*' % sub['name']
            d[sub['doctype']].update(['glottolog'])
            d['total'].update(['glottolog'])
            if gb_langs.intersection(set(sub['extension'])):
                d[sub['doctype']].update(['culturebank'])
                d['total'].update(['culturebank'])
            d['subgroups'][(sfid, sub['name'])] = dict(
                macroareas=spec['macroareas'],
                covered=gb_langs.intersection(set(sub['extension'])),
                grammar=Counter(),
                grammarsketch=Counter(),
                total=Counter())
            if not sub.get('subgroups'):
                # a language attached directly to the top-level family
                d['subgroups'][(sfid, sub['name'])][sub['doctype']].update(['glottolog'])
                d['subgroups'][(sfid, sub['name'])]['total'].update(['glottolog'])
                if gb_langs.intersection(set(sub['extension'])):
                    d['subgroups'][(sfid, sub['name'])][sub['doctype']].update(['culturebank'])
                    d['subgroups'][(sfid, sub['name'])]['total'].update(['culturebank'])
            for ssfid, ssub in list(sub.get('subgroups', {}).items()):
                if ssub['doctype']:
                    d['subgroups'][(sfid, sub['name'])][ssub['doctype']].update(['glottolog'])
                    d['subgroups'][(sfid, sub['name'])]['total'].update(['glottolog'])
                    if gb_langs.intersection(set(ssub['extension'])):
                        d['subgroups'][(sfid, sub['name'])][ssub['doctype']].update(['culturebank'])
                        d['subgroups'][(sfid, sub['name'])]['total'].update(['culturebank'])
        cstats[(fid, spec['name'])] = d

    return dict(
        stats=stats,
        cstats=cstats,
        macroareas=jsonload(
            abspath_from_asset_spec('culturebank:static/stats_macroareas.json')))
