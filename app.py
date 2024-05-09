from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ateflearns_user:your_secure_password@postgres/ateflearnsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Hello, World! This is Atef!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)