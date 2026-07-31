import unittest

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_dump_page_contains_request_details(self):
        response = self.client.get("/", headers={"X-Test-Header": "hello"})
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("CABEZA REQUEST DUMP", body)
        self.assertIn("X-Test-Header", body)
        self.assertIn("hello", body)


if __name__ == "__main__":
    unittest.main()
