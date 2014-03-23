import unittest
import transaction

from pyramid import testing

from .models import DBSession, Post


class TestViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            User,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            admin = User(name=u'admin', password=u'admin')
            post = Post(title=u'test', body=u'testbody')
            DBSession.add(admin)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_index(self):
        from .views import index_page
        request = testing.DummyRequest()
        info = index_page(request)
        self.assertEqual(info['paginator'].first().title, u'test')
        self.assertEqual(info['project'].first().body, u'testbody')
