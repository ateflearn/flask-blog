from app import db
from datetime import datetime
from sqlalchemy_utils import URLType

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_url = db.Column(URLType)

    def __repr__(self):
        return f'<BlogPost {self.title}>'
