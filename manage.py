from flask_script import Manager
from mint_api.main import app
from Crypto.PublicKey import RSA
import os
# ***** For Alembic start ******
from flask_migrate import Migrate, MigrateCommand
from mint_api.extensions import db

migrate = Migrate(app, db)
# ***** For Alembic end ******

manager = Manager(app)

# ***** For Alembic start ******
manager.add_command('db', MigrateCommand)


@manager.command
def runserver(port=8080):
    """Run the app using flask server"""

    os.environ["PYTHONUNBUFFERED"] = "yes"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["COMMIT"] = "LOCAL"

    app.run(debug=True, port=int(port))


@manager.command
def gen_test_keys():
    secret_key = os.environ["SECRET_KEY"]
    key = RSA.generate(2048)
    encrypted_key = key.exportKey(passphrase=secret_key)
    file_out = open("certs/test_private.pem", "wb")
    file_out.write(encrypted_key)
    public_key = key.publickey().exportKey()
    file_out = open("certs/test_public.pem", "wb")
    file_out.write(public_key)


if __name__ == "__main__":
    manager.run()
