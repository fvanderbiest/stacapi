import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import (
    Line,
    Stop
    )

from ..scrappers.stac import StacScrapper

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    s = StacScrapper()
    lines = s.get_lines()
    stops = s.get_stops()

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        
        dbsession.query(Stop).delete()
        dbsession.query(Line).delete()

        for l in lines:
            line = Line(
                id = l['id'],
                name = l['name'],
                direction1 = l['direction1'],
                direction2 = l['direction2'],
            )
            dbsession.add(line)
        dbsession.flush()

        for s in stops:
            stop = Stop(
                stac_id = s['id'],
                name = s['name'],
                order = s['order'],
                logical_id = s['logical_id'],
                line_id = s['line_id'],
            )
            dbsession.add(stop)

        #~ dbsession.commit() useless here
