from app import create_app
from app.models import db, User
import unittest
from app.utils.auth import generate_token, hash_password

class TestUser(unittest.TestCase):
  def setUp(self):
    self.app = create_app("TestingConfig")
    with self.app.app_context():
      db.drop_all()
      db.create_all()
      self.user = User(name="test_user", email="test@email.com", password=hash_password("test"))
      db.session.add(self.user)
      db.session.commit()
      self.token = generate_token(self.user.id)
    self.client = self.app.test_client()

  def test_create_user(self):
    user_payload = {
      "name": "John Doe",
      "email": "jd@email.com",
      "password": "test123"
    }
    
    response = self.client.post("/users/", json=user_payload)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.get_json()["name"], "John Doe")
    
  def test_invalid_user_creation(self):
    user_payload = {
      "name": "John Doe",
      "email": "jdoe@email.com"
    }
    
    response = self.client.post("/users/", json=user_payload)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.get_json()["password"], ["Missing data for required field."])
    
  def test_login_user(self):
    credentials = {
      "email": "test@email.com",
      "password": "test"
    }
    
    response = self.client.post("/users/login", json=credentials)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["status"], "success")
    return response.json["token"]
    
  def test_invalid_login(self):
    credentials = {
      "email": "bad_email@email.com",
      "password": "bad_pw"
    }
    
    response = self.client.post("/users/login", json=credentials)
    self.assertEqual(response.status_code, 401)
    self.assertEqual(response.json["error"], "Invalid email or password")
    
  def test_update_user(self):
    update_payload = {
      "name": "Peter"
    }
    
    headers = {"Authorization": f"Bearer {self.test_login_user()}"}
    
    response = self.client.patch("/users/", json=update_payload, headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["name"], "Peter")
    
  def test_delete_user(self):
    headers = {
      "Authorization": f"Bearer {self.token}"
    }
    
    response = self.client.delete("/users/", headers=headers)
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["message"], f"User {self.user.id} deleted successfully")