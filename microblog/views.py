from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from sqlalchemy.exc import DBAPIError

from .forms import BlogCreateForm, BlogUpdateForm

from .models import (
    DBSession,
    User,
    Post,
    )


@view_config(route_name='home', renderer='microblog:templates/index.mako')
def index_page(request):
    page = int(request.params.get('page', 1))
    paginator = Post.get_paginator(request, page)
    return {'paginator': paginator}


@view_config(route_name='blog', renderer='microblog:templates/view_blog.mako')
def blog_view(request):
    id = int(request.matchdict.get('id', -1))
    post = Post.by_id(id)
    if not post:
        return HTTPNotFound()
    return {'post': post}


@view_config(route_name='blog_action', match_param='action=create',
             renderer='microblog:templates/edit_blog.mako')
def blog_create(request):
    post = Post()
    form = BlogCreateForm(request.post)
    if request.method == 'POST' and form.validate:
        form.populate_obj(post)
        DBSession.add(post)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='microblog:templates/edit_blog.mako')
def blog_update(request):
    id = int(request.params.get('id', -1))
    post = Post.by_id(id)
    if not post:
        return HTTPNotFound
    form = BlogUpdateForm(request.POST, post)
    if request.method == 'POST' and form.validate():
        form.populate_obj(post)
        return HTTPFound(location=request.route_url('blog', id=post.id,
                                                    slug=post.slug))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    return {}
