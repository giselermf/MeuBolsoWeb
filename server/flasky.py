from flask_migrate import Migrate
from server.app import create_app, db

app = create_app('production')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
migrate = Migrate(app, db)

