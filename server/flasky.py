from flask_migrate import Migrate
from server.app import create_app, db
# from flask_marshmallow import Marshmallow

app = create_app('production')
# ma = Marshmallow(app)
migrate = Migrate(app, db)
