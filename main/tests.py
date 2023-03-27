from collections import OrderedDict

from django.test import TestCase, Client
from rest_framework.test import APITestCase

from main.models import User, Bug

# Create your tests here.


class PersonTestCase(TestCase):
    def test_no_people(self):
        client = Client()
        response = client.get("/")
        self.assertInHTML("<ul></ul>", response.content.decode())

    def test_create_person(self):
        client = Client()
        response = client.post("/newperson", {"name": "Test Person"})
        person = User.objects.get(name="Test Person")
        response = client.get("/")
        self.assertInHTML('<span id="person%d">Test Person (0 open bugs)&nbsp;</span>' % person.id, response.content.decode())

    def test_rename_person(self):
        client = Client()
        person = User(name="Test Person")
        person.save()
        response = client.post("/person", {"name": "Edited Person", "personid": person.id})
        response = client.get("/")
        self.assertInHTML("""<span id="person%d">Edited Person (0 open bugs)&nbsp;</span>""" % person.id, response.content.decode())


class BugTestCase(TestCase):
    def setUp(self):
        User(name="Test Person").save()

    def test_no_bugs(self):
        client = Client()
        response = client.get("/")
        self.assertInHTML("<tbody></tbody>", response.content.decode())

    def test_create_bug(self):
        client = Client()
        person = User.objects.get(name="Test Person")
        response = client.post("/newbug", {"title": "A Test Bug", "owner": person.id, "text": "This is a test bug, used for testing"})
        response = client.get("/")
        self.assertInHTML("<td>A Test Bug</td><td>Test Person</td><td>Open</td>", response.content.decode())

    def test_close_bug(self):
        client = Client()
        person = User.objects.get(name="Test Person")
        bug = Bug(title="An open bug", owner=person, text="This bug should be closed")
        bug.save()
        response = client.post("/closebug/%d" % bug.id)
        response = client.get("/")
        self.assertInHTML("<td>An open bug</td><td>Test Person</td><td>Closed</td>", response.content.decode())

    def test_close_bug_twice(self):
        client = Client()
        person = User.objects.get(name="Test Person")
        bug = Bug(title="An open bug", owner=person, text="This bug should be closed")
        bug.save()
        response = client.post("/closebug/%d" % bug.id)
        response = client.post("/closebug/%d" % bug.id)
        response = client.get("/")
        self.assertInHTML("""<div class="alert alert-dismissible fade show alert-danger">Cannot close bug - already closed<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>""", response.content.decode())


class PersonAPITestCase(APITestCase):
    def test_no_people(self):
        response = self.client.get("/api/people")
        self.assertEqual(response.data, [])

    def test_create_person(self):
        response = self.client.post("/api/person", {"name": "Test Person"})
        person = User.objects.get(name="Test Person")
        response = self.client.get("/api/people")
        self.assertEqual(response.data, [{"id": person.id, "name": "Test Person"}])

    def test_rename_person(self):
        person = User(name="Test Person")
        person.save()
        response = self.client.post("/api/person%d" % person.id, {"name": "Edited Person"})
        response = self.client.get("/api/people")
        self.assertEqual(response.data, [OrderedDict([('id', person.id), ('name', 'Test Person')])])


class BugAPITestCase(APITestCase):
    def setUp(self):
        User(name="Test Person").save()

    def test_no_bugs(self):
        response = self.client.get("/api/bugs")
        self.assertEqual(response.data, [])

    def test_create_bug(self):
        person = User.objects.get(name="Test Person")
        response = self.client.post("/api/bug", {"title": "A Test Bug", "owner": person.id, "text": "This is a test bug, used for testing"})
        response = self.client.get("/api/bugs")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "A Test Bug")
        self.assertEqual(response.data[0]['owner'], person.id)
        self.assertEqual(response.data[0]['text'], "This is a test bug, used for testing")
        self.assertEqual(response.data[0]['closed'], False)

    def test_close_bug(self):
        person = User.objects.get(name="Test Person")
        bug = Bug(title="An open bug", owner=person, text="This bug should be closed")
        bug.save()
        response = self.client.post("/api/bug/%d" % bug.id, {"title": bug.title, "text": bug.text, "owner": bug.owner_id, "closed": True})
        response = self.client.get("/api/bugs")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["closed"], True)
