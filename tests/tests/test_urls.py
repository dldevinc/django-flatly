import pytest
from django.test.client import Client


@pytest.mark.django_db
class TestAppendSlash:
    def setup(self):
        self.client = Client()

    def test_admin_append_slash(self):
        response = self.client.get('/admin/login')
        assert response.status_code == 200

    def test_admin_with_slash(self):
        response = self.client.get('/admin/login/')
        assert response.status_code == 200

    def test_flatly_append_slash(self):
        response = self.client.get('/app')
        assert response.status_code == 200

    def test_flatly_with_slash(self):
        response = self.client.get('/app/')
        assert response.status_code == 200

    def test_missing(self):
        response = self.client.get('/missing')
        assert response.status_code == 404
