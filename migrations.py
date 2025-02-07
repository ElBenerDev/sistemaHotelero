from flask_migrate import Migrate
from src import create_app
from src.extensions import db

app = create_app()
migrate = Migrate(app, db)