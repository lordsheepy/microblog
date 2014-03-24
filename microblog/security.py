from pyramid.security import Allow, Everyone, Authenticated, ALL_PERMISSIONS


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
