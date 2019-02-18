from flask_migrate import Migrate
from server.app import create_app, db

app = create_app('production')
migrate = Migrate(app, db)

