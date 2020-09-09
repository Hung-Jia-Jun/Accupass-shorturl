import flask
import unittest
import flask_testing
from app import app
    
class TestShortUrlApp(flask_testing.TestCase):
    def create_app(self):
        return app
    def test_get_shortUrl_index(self):
        with app.test_client() as lTestClient:
            resp = lTestClient.get('/')
            self.assertEqual(resp.status_code, 200)
            print (resp.data)
            self.assertContains(resp.text, "已幫您將網址轉換為")

if __name__ == "__main__":
    unittest.main()