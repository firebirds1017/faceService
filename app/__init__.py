from flask import Flask
from config import configs


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(configs[config_name])
    configs[config_name].init_app()
    from .face import face as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/face')

    return app
