import transaction
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.security import remember, forget, authenticated_userid


from sqlalchemy.exc import DBAPIError

from .forms import BlogCreateForm, BlogUpdateForm, CreateUser
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from .models import (
    DBSession,
    User,
    Post,
    TempUser,
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


@view_config(route_name='blog_create', match_param='action=create',
             renderer='microblog:templates/edit_blog.mako',
             permission='create')
def blog_create(request):
    post = Post()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate:
        form.populate_obj(post)
        post.owner = authenticated_userid(request)
        DBSession.add(post)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action')}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='microblog:templates/edit.mako',
             permission='edit')
def blog_update(context, request):
    post = context
    if not post:
        return HTTPNotFound
    form = BlogUpdateForm(request.POST, post)
    if request.method == 'POST' and form.validate():
        form.populate_obj(post)
        return HTTPFound(location=request.route_url('blog', id=post.id,
                                                    slug=post.slug))
    return {'form': form, 'action': request.matchdict.get('action'),
            'id': post.id}


@view_config(route_name='blog_action', match_param='action=del',
             renderer='microblog:templates/edit_blog.mako',
             permission='edit')
def blog_delete(context, request):
    post = context
    if not post:
        return HTTPNotFound
    DBSession.delete(post)
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = User.by_name(username)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)


@view_config(route_name='register',
             renderer='microblog:templates/register.mako')
def register(request):
    user = TempUser()
    form = CreateUser(request.POST)
    if request.method == 'POST' and form.validate:
        form.populate_obj(user)
        DBSession.add(user)
        body = """Click this link to confirm your registration:
    www.shrikelight.com/confirm/%s""" % user.verify
        message = Message(subject="Your Pyramid Microblog Registration",
                          sender="pyramid.microblog@gmail.com",
                          recipients=[user.email],
                          body=body)
        mailer = get_mailer(request)
        mailer.send_immediately(message)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}


@view_config(route_name='confirm', renderer='string')
def confirm(request):
    verify = int(request.matchdict.get('verify', False))
    tempuser = TempUser.by_verify(verify)
    tempuser.upgrade()
    return HTTPFound(location=request.route_url('home'))
