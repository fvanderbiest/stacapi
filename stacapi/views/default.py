from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Line


@view_config(route_name='home', renderer='../templates/index.jinja2')
def my_view(request):
    return {}
    #~ try:
        #~ query = request.dbsession.query(Line)
        #~ one = query.filter(Line.name == 'A').first()
    #~ except DBAPIError:
        #~ return Response(db_err_msg, content_type='text/plain', status=500)
    #~ return {'one': one, 'project': 'stacapi'}
    #~ return {'direction1': one.direction1, 'direction2': one.direction2, 'project': 'stacapi'}
