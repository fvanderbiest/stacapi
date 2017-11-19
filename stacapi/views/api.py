from cornice.resource import resource, Service

from pyramid.security import Allow

from pyramid.httpexceptions import (
    HTTPNotFound, HTTPInternalServerError,
    HTTPNotImplemented)

from ..models import Line, Stop
from ..utils import query


realtime = Service(name='realtime',
                   path='/realtime/{lineid}/{stopid}/{direction}',
                   description='Proxy to STAC real time services.')


@realtime.get()
def realtime_proxy(request):
    """Proxy to STAC realtime services
    """
    lineId = request.matchdict['lineid']
    stopId = request.matchdict['stopid']
    direction = request.matchdict['direction']
    
    DBSession = request.dbsession
    buses = query(lineId, stopId, direction, DBSession)
    return {"nextbuses": buses}


@resource(collection_path='/lines', path='/lines/{id}')
class LineResource(object):
 
    def __init__(self, request):
        self.request = request

    def __acl__(self):
        return [(Allow, Everyone, 'view')]

    def get(self):
        id = self.request.matchdict['id']
        DBSession = self.request.dbsession
        line = None
        try:
            line = DBSession.query(Line).filter(Line.id==id).one_or_none()
        except:
            raise HTTPInternalServerError("There was an error querying the db")
        finally:
            if line:
                return line.to_json()
            else:
                raise HTTPNotFound("The object does not exist")
                #~ return HTTPUnprocessableEntity(body=json.dumps(id))

    def collection_get(self):
        DBSession = self.request.dbsession
        return {'lines': [line.to_json() for line in DBSession.query(Line)]}
 
    def collection_post(self):
        raise HTTPNotImplemented("This is a read-only API")

@resource(collection_path='/stops', path='/stops/{id}')
class StopResource(object):
 
    def __init__(self, request):
        self.request = request

    def __acl__(self):
        return [(Allow, Everyone, 'view')]

    def get(self):
        stac_id = self.request.matchdict['id']
        DBSession = self.request.dbsession
        stop = None
        try:
            stop = DBSession.query(Stop).filter(Stop.stac_id==stac_id).one_or_none()
        except:
            raise HTTPInternalServerError("There was an error querying the db")
        finally:
            if stop:
                return stop.to_json()
            else:
                raise HTTPNotFound("The object does not exist") 
                #~ return HTTPUnprocessableEntity(body=json.dumps(id))

    def collection_get(self):
        DBSession = self.request.dbsession
        return {'stops': [stop.to_json() for stop in DBSession.query(Stop)]}
 
    def collection_post(self):
        raise HTTPNotImplemented("This is a read-only API")
