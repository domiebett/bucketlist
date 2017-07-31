#env/bin/.Python

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bucketlist import create_app
from bucketlist.models import db


config_name = os.environ.get("APP_CONFIG")

app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()

if __name__ == '__main__':
    manager.run()
