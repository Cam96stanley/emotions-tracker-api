from dotenv import load_dotenv
from app import create_app
from app.models import db
from app.seeders.seed_moods import seed_moods

load_dotenv()

app = create_app("ProductionConfig")

with app.app_context():
  db.create_all()
  seed_moods()