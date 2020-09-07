# coding:utf-8
 
import unittest
import app
import json
 
 
class TestLogin(unittest.TestCase):
    def setUp(self):
        app.testing = True  
        self.client = app.test_client()
    
    def test_vaildurlshort(self):
        response = self.client.post("/dologin", data={})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
 
        code = resp_dict.get("code")
        self.assertEqual(code, 1)
 
 