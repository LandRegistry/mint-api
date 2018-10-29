# Import every blueprint file
from mint_api.views import general
from mint_api.views.v1_0 import signing as signing1_0


def register_blueprints(app):
    """Adds all blueprint objects into the app.

    """
    app.register_blueprint(general.general)
    app.register_blueprint(signing1_0.signing, url_prefix='/v1.0')

    # All done!
    app.logger.info("Blueprints registered")
