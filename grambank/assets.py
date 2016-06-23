from clld.web.assets import environment
from clldutils.path import Path

import culturebank


environment.append_path(
    Path(culturebank.__file__).parent.joinpath('static').as_posix(), url='/culturebank:static/')
environment.load_path = list(reversed(environment.load_path))
