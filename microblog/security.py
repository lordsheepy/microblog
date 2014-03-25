from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS
from .models import Post


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'create'),
        (Allow, Everyone, 'view'),
        (Allow, 'admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        pass


class PostFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'create'),
        (Allow, 'admin', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        # import pdb; pdb.set_trace()
        post = Post.by_id(key)
        post.__parent__ = self
        post.__name__ = key
        return post
