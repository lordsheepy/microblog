from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS


POSTS = {}


class PostFactory(object):
    __acl__ = [
        (Allow, 'admin', ALL_PERMISSIONS),
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'create'),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        post = POSTS[key]
        post.__parent__ = self
        post.__name__ = key
        return post
