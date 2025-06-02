from app import create_app
from app.models import db, UserMood, User, Feeling, Mood
import unittest

from app.utils.auth import generate_token, hash_password

class TestUser(unittest.TestCase):
  def setUp(self):
    self.app = create_app("TestingConfig")
    with self.app.app_context():
      db.drop_all()
      db.create_all()
      self.user = User(name="test_user", email="test@test.com", password=hash_password("test"))
      self.feeling = Feeling(feeling_name="excited")
      self.mood = Mood(mood_type="Happy")
      db.session.add_all([self.user, self.feeling, self.mood])
      db.session.commit()
      self.user_id = self.user.id
      self.feeling_id = self.feeling.id
      self.mood_id = self.mood.id
      self.token = generate_token(self.user.id)
    self.client = self.app.test_client()
    
  def test_create_usermood(self):
    usermood_payload = {
      "user": self.user_id,
      "mood": self.mood_id,
      "diary_entry": "I'm so excited",
      "sleep_time": 8,
      "feelings": [self.feeling.id]
    }
    
    headers = {
      "Authorization": f"Bearer {self.token}"
    }
    
    response = self.client.post("/usermoods/", json=usermood_payload, headers=headers)
    
    self.assertEqual(response.status_code, 201)
    self.assertIn("diary_entry", response.json)
    self.assertEqual(response.json["diary_entry"], "I'm so excited")
    
  def test_get_usermoods(self):
    with self.app.app_context():
      usermood = UserMood(
        user=self.user,
        mood=self.mood,
        diary_entry="Feeling great",
        sleep_time=8
      )
      
      usermood.feelings.append(self.feeling)
      db.session.add(usermood)
      db.session.commit()
      
    headers = {
      "Authorization": f"Bearer {self.token}"
    }
    
    response = self.client.get("/usermoods/", headers=headers)
    
    self.assertEqual(response.status_code, 200)
    self.assertIsInstance(response.json, list)
    self.assertGreater(len(response.json), 0)
    self.assertEqual(response.json[0]["diary_entry"], "Feeling great")
    
  def test_delete_usermood(self):
    with self.app.app_context():
        usermood = UserMood(
            user=self.user,
            mood=self.mood,
            diary_entry="Mood to delete",
            sleep_time=7
        )
        usermood.feelings.append(self.feeling)
        db.session.add(usermood)
        db.session.commit()

        usermood_id = usermood.id

    headers = {
        "Authorization": f"Bearer {self.token}"
    }

    response = self.client.delete(f"/usermoods/{usermood_id}", headers=headers)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json["message"], "UserMood deleted successfully")