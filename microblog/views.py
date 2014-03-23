from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    )


@view_config(route_name='home', renderer='microblog:templates/index.mako')
def index_page(request):
    return {}


@view_config(route_name='blog', renderer='microblog:templates/view_blog.mako')
def blog_view(request):
    return {}


@view_config(route_name='blog_action', match_param='action=create',
             renderer='microblog:templates/edit_blog.mako')
def blog_create(request):
    return {}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='microblog:templates/edit_blog.mako')
def blog_update(request):
    return {}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    return {}
