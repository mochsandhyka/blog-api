from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from app.prefix_middleware import PrefixMiddleware

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app,db)
CORS(app)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/blog-api/v1')


from app.models import user, address


from app import routes
if __name__ == "__main__":
    app.run()