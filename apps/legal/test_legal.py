import pytest
from inertia.test import InertiaTestCase

DOCUMENTS_FIXTURE = {
    "privacy": {
        "title": "Политика конфиденциальности",
        "updated_at": "2026-07-01",
    },
    "agreement": {
        "title": "Пользовательское соглашение",
        "updated_at": "2026-07-01",
    },
    "offer": {
        "title": "Публичная оферта",
        "updated_at": "2026-07-01",
    },
}


@pytest.mark.django_db
def test_documents_view(client):
    # GET-запрос
    response = client.get("/legal/")

    assert response.status_code == 200


class LegalViewTestCase(InertiaTestCase):
    def test_show_assertions(self):
        self.client.get("/legal/")

        self.assertComponentUsed("Legal")
