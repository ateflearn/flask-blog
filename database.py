from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{app.config["POSTGRES_USER"]}:' \
                                            f'{app.config["POSTGRES_PASSWORD"]}@' \
                                            f'{app.config["POSTGRES_HOST"]}/' \
                                            f'{app.config["POSTGRES_DB"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    Migrate(app, db)
