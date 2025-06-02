from app import create_app
from app.models import db, Feeling
import unittest

class TestUser(unittest.TestCase):
  def setUp(self):
    self.app = create_app("TestingConfig")
    with self.app.app_context():
      db.drop_all()
      db.create_all()
    self.client = self.app.test_client()
    
  def test_create_feeling(self):
    feeling_payload = {
      "feeling_name": "Excited"
    }
    
    response = self.client.post("/feelings/", json=feeling_payload)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json["feeling_name"], "Excited")