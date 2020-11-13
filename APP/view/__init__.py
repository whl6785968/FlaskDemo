from .first import blue
from .second import second

def init_view(app):
    app.register_blueprint(blue)
    app.register_blueprint(second)