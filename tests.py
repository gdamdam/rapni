"""
tests.py

some test for Rapni app

:copyright: (C) 2016 Internet Archive.
:   author: Giovanni Damiola <gio@archive.org>
"""

import unittest
from rapni import app
import tempfile
import config

class IabDashTest(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.delete('/docs/test_item',headers={'Authorization': config.AUTH_TOKEN})

    def test_docs(self):
        rv = self.app.get('/')
        self.assertEquals(200,rv.status_code)

    def test_insert_and_delete_id_docs(self):
        rv = self.app.post('/docs/test!#@item', headers={'Authorization': config.AUTH_TOKEN,'Content-Type':'application/json'}, data='{"location":"san_francisco","operator":"test@example.org"}', follow_redirects=True)
        self.assertEquals(406,rv.status_code)
        rv = self.app.post('/docs/test_item', headers={'Authorization': config.AUTH_TOKEN,'Content-Type':'application/json'}, data='{"location":"san_francisco","operator":"test@example.org"}', follow_redirects=True)
        self.assertEquals(201,rv.status_code)
        rv = self.app.delete('/docs/test_item',headers={'Authorization': config.AUTH_TOKEN})
        self.assertEquals(200,rv.status_code)

    def test_update_docs(self):
        rv = self.app.post('/docs/test_item', headers={'Authorization': config.AUTH_TOKEN,'Content-Type':'application/json'}, data='{"location":"san_francisco","operator":"test@example.org"}', follow_redirects=True)
        self.assertEquals(201,rv.status_code)
        rv = self.app.get('/docs/test_item')
        assert '"location": "san_francisco"' in rv.data
        rv = self.app.put('/docs/test_item', headers={'Authorization': config.AUTH_TOKEN,'Content-Type':'application/json'}, data='{"location":"london","type":"test","operator":"test@example.org"}', follow_redirects=True)
        self.assertEquals(200,rv.status_code)
        rv = self.app.get('/docs/test_item')
        assert '"location": "london"' in rv.data
        rv = self.app.delete('/docs/test_item', headers={'Authorization': config.AUTH_TOKEN})
        self.assertEquals(200,rv.status_code)


    def test_add_event(self):
        rv = self.app.post('/events', headers={ 'Authorization': config.AUTH_TOKEN,'Content-Type':'application/json'}, data='{"target":"terget001","type":"docs","operator":"test@example.org"}', follow_redirects=True)
        self.assertEquals(201,rv.status_code)
        rv = self.app.post('/events', headers={ 'Authorization': config.AUTH_TOKEN}, data='{"type":"docs","operator":"test@example.org"}', follow_redirects=True)
        self.assertEquals(406,rv.status_code)

    def test_get_location_docs(self):
        rv = self.app.post('/docs/test_item', headers={'Authorization': config.AUTH_TOKEN,'Content-Type':'application/json'}, data='{"location":"testcenter","operator":"test@example.org"}', follow_redirects=True)
        self.assertEquals(201,rv.status_code)
        rv = self.app.get('/docs/testcenter/documents', headers={ 'Authorization': config.AUTH_TOKEN,'Content-Type':'application/json'}, follow_redirects=True)
        assert '"location": "london"' not in rv.data
        assert '"location": "testcenter"' in rv.data
        rv = self.app.delete('/docs/test_item',headers={'Authorization': config.AUTH_TOKEN})
        self.assertEquals(200,rv.status_code)



if __name__ == '__main__':
    unittest.main(verbosity=2)
