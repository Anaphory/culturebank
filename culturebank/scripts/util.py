
import os
import re
from collections import OrderedDict
from itertools import cycle
import csv
import pandas
import getpass

from nameparser import HumanName

from clldutils.jsonlib import load as jsonload
from clldutils.misc import slug
from clldutils.dsv import reader
from clldutils.path import Path

from clld.db.meta import DBSession
from clld.db.models.common import (
    ValueSet, Value, DomainElement, Source, ValueSetReference,
    ContributionContributor, Contributor,
)
from clld.lib.bibtex import Database
from clld.web.icon import ORDERED_ICONS
from clld.scripts.util import bibtex2source

from clldclient.glottolog import Glottolog

import culturebank
from culturebank.models import CulturebankLanguage, Feature, CulturebankContribution


CULTUREBANK_REPOS = "j:/ResearchData/HUM/LUCL-KlamerVICI/sunda_database/culturerumah-data/"

def import_dataset(path, data, icons, add_missing_features = False):
    # look for metadata
    # look for sources
    # then loop over values
    
    dirpath, fname = os.path.split(path)
    basename, ext = os.path.splitext(fname)
    glottolog = Glottolog()

    try:
        contrib = CulturebankContribution(id=basename, name=basename, desc=glottolog.languoid(basename).name)
    except:
        print("Basename {:s} did not match a glottolog languoid, skipped.".format(basename))
        return

    md = {}
    mdpath = path + '-metadata.json'
    if os.path.exists(mdpath):
        md = jsonload(mdpath)
    contributor_name = HumanName(md.get('contributed_datapoint', 'Team NTS'))
    contributor_id = slug(contributor_name.last + contributor_name.first)
    contributor = data['Contributor'].get(contributor_id)
    if not contributor:
        contributor = data.add(
            Contributor,
            contributor_id,
            id=contributor_id,
            name='%s' % contributor_name)
    DBSession.add(ContributionContributor(contribution=contrib, contributor=contributor))

    bibpath = os.path.join(dirpath, basename + '.bib')
    if os.path.exists(bibpath):
        for rec in Database.from_file(bibpath):
            if rec['key'] not in data['Source']:
                data.add(Source, rec['key'], _obj=bibtex2source(rec))

    languages = {f['properties']['glottocode']: f for f in md.get('features', [])}

    for i, row in pandas.io.parsers.read_csv(
            path,
            sep=',' if 'c' in ext else '\t',
            encoding='utf-16').iterrows():
        if pandas.isnull(row['Value']) or pandas.isnull(row['Feature_ID']):
            print("Expected columns not found: ", row)
            continue
        vsid = '%s-%s-%s' % (basename, row['Language_ID'], row['Feature_ID'])
        vid = row.get('ID', '%s-%s' % (basename, i + 1))

        parameter = data['Feature'].get(row['Feature_ID'])
        if parameter is None:
            if add_missing_features:
                parameter = data.add(Feature, row['Feature_ID'], id=row['Feature_ID'], name=row.get('Feature', row['Feature_ID']))
            else: 
                print(('skip value for invalid feature %s' % row['Feature_ID']))
                continue

        language = data['CulturebankLanguage'].get(row['Language_ID'])
        if language is None:
            # query glottolog!
            try:
                languoid = glottolog.languoid(row['Language_ID'])
            except AttributeError:
                print(('Skipping, no Glottocode found for %s' % row['Language_ID']))
                continue
            
            gl_md = {
                'name': languoid.name,
                'longitude': languoid.longitude,
                'latitude': languoid.latitude}
            lmd = languages.get(row['Language_ID'])
            if lmd:
                if lmd.get('properties', {}).get('name'):
                    gl_md['name'] = lmd['properties']['name']
                if lmd.get('geometry', {}).get('coordinates'):
                    gl_md['longitude'], gl_md['latitude'] = lmd['geometry']['coordinates']

            language = data.add(
                CulturebankLanguage, row['Language_ID'],
                id=row['Language_ID'],
                name=gl_md['name'],
                latitude=gl_md.get('latitude'),
                longitude=gl_md.get('longitude'))

        
        vs = data['ValueSet'].get(vsid)
        if vs is None:
            vs = data.add(
                ValueSet, vsid,
                id=vsid,
                parameter=parameter,
                language=language,
                contribution=contrib,
                source=row['Source'])

        domain = {de.abbr: de for de in parameter.domain}    
        name = row['Value']
        if name in domain:
            name = domain[name].name
        else:
            name = str(name)
            if name in domain:
                name = domain[name].name
            else:
                raise ValueError("For feature {:s} in language {:s}: Name {:s} not found among domain values {:}".format(
                    row['Language_ID'],
                    row['Feature_ID'],
                    name,
                    {d: de for d, de in domain.items()}))

        data.add(Value,
            vid,
            id=vid,
            valueset=vs,
            name=name,
            description=row['Comment'],
            domainelement=domain.get(row['Value']))

        print(".", end="")
        if vs.source is not None:
            for key, src in list(data['Source'].items()):
                if key in vs.source:
                    ValueSetReference(valueset=vs, source=src, key=key)


def import_cldf(srcdir, data, add_missing_features = False):
    # loop over values
    # check if language needs to be inserted
    # check if feature needs to be inserted
    # add value if in domain
    icons = cycle(ORDERED_ICONS)
    for dirpath, dnames, fnames in os.walk(srcdir):
        for fname in fnames:
            if os.path.splitext(fname)[1] in ['.tsv', '.csv']:
                try:
                    import_dataset(os.path.join(dirpath, fname), data, icons, add_missing_features = add_missing_features)
                    print(os.path.join(dirpath, fname))
                except:
                    print('ERROR')
                    raise
                #break

    pass


class FeatureSpec(object):
    @staticmethod
    def yield_domainelements(s):
        try:
            for m in re.split('\s*,|;\s*', re.sub('^multistate\s+', '', s.strip())):
                if m.strip():
                    if m.startswith('As many'):
                        for i in range(100):
                            yield '%s' % i, '%s' % i
                    else:
                        number, desc = m.split(':')
                        yield number.strip(), desc.strip()
        except:
            print(s)
            raise

    def __init__(self, d):
        self.id = d['CultureBank ID'].strip()
        self.name = d['Feature']
        self.doc = d['Clarifying Comments']
        self.patron = d['Feature patron']
        self.std_comments = d['Suggested standardised comments']
        self.name_french = d['Feature question in French']
        self.jl_relevant_unit = d['Relevant unit(s)']
        self.jl_function = d['Function']
        self.jl_formal_means = d['Formal means']
        self.hard_to_deny = d['Very hard to deny']
        self.prone_misunderstanding = d['Prone to misunderstandings among researchers']
        self.requires_extensive_data = d['Requires extensive data on the language']
        self.last_edited = d['Last edited']
        self.other_survey = d['Is there a typological survey that already covers this feature somehow?']
        self.domain = OrderedDict()
        for n, desc in self.yield_domainelements(d['Possible Values']):
            self.domain[n] = desc
        self.domain.update({'?': 'Not known'})

    def format_domain(self):
        return '; '.join('%s: %s' % item for item in list(self.domain.items()) if item[0] != '?')


def import_features_collaborative_sheet(datadir, data):
    for i, feature in pandas.io.parsers.read_csv(
            os.path.join(datadir, 'features_collaborative_sheet.tsv'),
            sep='\t', encoding='utf-16').iterrows():
        feature = FeatureSpec(feature)
        f = data.add(Feature, feature.id, id=feature.id, name=feature.name, doc=feature.doc, patron=feature.patron, std_comments=feature.std_comments, name_french=feature.name_french, jl_relevant_unit=feature.jl_relevant_unit, jl_function=feature.jl_function, jl_formal_means=feature.jl_formal_means, hard_to_deny=feature.hard_to_deny, prone_misunderstanding=feature.prone_misunderstanding, requires_extensive_data=feature.requires_extensive_data, last_edited=feature.last_edited, other_survey=feature.other_survey)
        for i, (deid, desc) in enumerate(feature.domain.items()):
            DomainElement(
                id='%s-%s' % (f.id, deid),
                parameter=f,
                abbr=deid,
                name='%s - %s' % (deid, desc),
                number=int(deid) if deid != '?' else 999,
                description=desc,
                jsondata=dict(icon=ORDERED_ICONS[i].name))


def get_clf_paths(lgs):
    glottolog = Glottolog()
    for lg in lgs:
        l = glottolog.languoid(lg)
        ancestors = [l.id]
        while l.parent:
            ancestors.insert(0, l.parent.id)
            l = l.parent
        yield tuple(ancestors)

def get_name(l_id):
    return Glottolog().languoid(l_id).name
