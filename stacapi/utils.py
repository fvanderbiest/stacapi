import sys
import requests
from json import loads
from datetime import datetime

import transaction

from pyramid.paster import get_appsettings

from pyramid.scripts.common import parse_vars

from .models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from .models.models import Stop


def query(lineId, stopId, direction, dbsession = None):

    BASEURL = "https://www.bus-stac.fr"

    # find logicalStopId based on lineId, stopId
    if dbsession:
        stop = dbsession.query(Stop).filter_by(line_id = lineId, stac_id = stopId).one_or_none()
        if stop is None:
            print("Could not find stop logical_id")
            sys.exit(1) # FIXME: raise exception
        logicalStopId = stop.logical_id
    else:
        settings = get_appsettings("development.ini")
        engine = get_engine(settings)
        session_factory = get_session_factory(engine)

        with transaction.manager:
            dbsession = get_tm_session(session_factory, transaction.manager)
            stop = dbsession.query(Stop).filter_by(line_id = lineId, stac_id = stopId).one_or_none()
            if stop is None:
                print("Could not find stop logical_id")
                sys.exit(1)
            logicalStopId = stop.logical_id

    referer = ("{}/Se-deplacer/Horaires-passage-temps-reel?"
        "schedules_by_stop[stopId]={}&"
        "schedules_by_stop[logicalStopId]={}&"
        "schedules_by_stop[lineId]={}&"
        "schedules_by_stop[direction]={}").format(
            BASEURL,
            stopId,
            logicalStopId,
            lineId,
            direction)

    requests.packages.urllib3.disable_warnings()
    r = requests.post("{}/get-next-stop-time".format(BASEURL),
        data=("schedules_by_stop[direction]=1&"
            "schedules_by_stop[lineId]={}").format(lineId), 
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "Referer": referer
        },
        verify=False
    )

    etas = loads(r.text)
    now = datetime.now()

    out = []
    for nextbus in etas:
        date = datetime.strptime(nextbus, '%Y-%m-%dT%H:%M:%S+02:00')
        delta = date - now
        minutes = round(delta.total_seconds() // 60)
        seconds = round(delta.total_seconds() % 60)
        out.append({"min": minutes, "sec": seconds, "time": date.strftime("%H:%M")})

    return out;