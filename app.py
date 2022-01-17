from flask import Flask

from api_users import api_users
from database import db_session

app = Flask(__name__)
app.register_blueprint(api_users)


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()
