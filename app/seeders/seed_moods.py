from app.models import db, Mood

def seed_moods():
  predefined_moods = ["happy", "neutral", "sad"]
  existing_moods = {mood.name for mood in db.session.query(Mood).all()}
  
  for mood_name in predefined_moods:
    if mood_name not in existing_moods:
      db.session.add(Mood(mood_type=mood_name))
      
  db.session.commit()