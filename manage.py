from flask_script import Manager

from APP import create_app
import os

env = os.environ.get('FLASK_ENV','develop')

app = create_app(env=env)
manager = Manager(app=app)


if __name__ == '__main__':
    manager.run()
