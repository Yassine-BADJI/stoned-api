import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from model import User, Types, Drugs, Takes
from app import create_app, db

app = create_app(os.getenv('ENV_STATUS') or 'prod')
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
