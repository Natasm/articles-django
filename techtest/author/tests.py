import json

from django.test import TestCase
from django.urls import reverse

from techtest.author.models import Author


class AuthorListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("author-list")
        self.author1 = Author.objects.create(
            first_name="Natan", last_name="Morais"
        )
        self.author2 = Author.objects.create(
            first_name="NS", last_name="Morais"
        )

    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            [
                {
                    "id": self.author1.id,
                    "first_name": "Natan",
                    "last_name": "Morais"
                },
                {
                    "id": self.author2.id,
                    "first_name": "NS",
                    "last_name": "Morais"
                },
            ],
        )

    def test_creates_new_author(self):
        payload = {
            "first_name": "Tulio",
            "last_name": "Jander"
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(author)
        self.assertDictEqual(
            {
                "id": author.id,
                "first_name": "Tulio",
                "last_name": "Jander"
            },
            response.json(),
        )


class AuthorViewTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            first_name="Natan", last_name="Morais"
        )
        self.url = reverse("author", kwargs={"author_id": self.author1.id})

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            {
                "id": self.author1.id,
                "first_name": "Natan",
                "last_name": "Morais"
            },
        )

    def test_update_author(self):
        # Change authors
        payload = {
            "first_name": "Natan",
            "last_name": "Morais (Modified)"
        }
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(author)
        self.assertDictEqual(
            {
                "id": author.id,
                "first_name": "Natan",
                "last_name": "Morais (Modified)"
            },
            response.json(),
        )

    def test_removes_author(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Author.objects.count(), 0)
