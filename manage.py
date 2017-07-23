#env/bin/.Python

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bucketlist.views import create_app
from bucketlist.models import db, User, BucketList, ListItem

app = create_app('dev')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
