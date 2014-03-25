from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import Root, PostFactory
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authentication_policy = AuthTktAuthenticationPolicy('secretkey')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          root_factory=Root,
                          )
    config.include('pyramid_mailer')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('blog', '/blog/{id:\d+}/{slug}')
    config.add_route('blog_action', '/blog/{action}/{id}', factory=PostFactory,
                     traverse='/{id}')
    config.add_route('blog_create', '/blog/{action}')
    config.add_route('auth', '/sign/{action}')
    config.add_route('register', '/register')
    config.add_route('confirm', '/confirm/{verify:\d+}')
    config.scan()
    return config.make_wsgi_app()
