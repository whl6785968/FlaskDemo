from flask import Flask

from APP.Api import init_api
from APP.ext import init_ext
from APP.settings import envs
from APP.view import init_view

def create_app(env):
    app = Flask(__name__)

    app.config.from_object(envs.get(env))
    init_ext(app=app)
    init_view(app=app)
    init_api(app=app)
    return app