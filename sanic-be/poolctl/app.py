"""
Sanic application factory module.

"""
from sanic import Sanic
from sanic_cors import CORS


def create_app() -> Sanic:
    app = Sanic('poolctl-be', load_env=False)
    CORS(app)  # TODO: Revisit security
    return app


app = create_app()
