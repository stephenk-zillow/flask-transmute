import json
from flask import Response, Blueprint
from swagger_schema import Swagger, Info

from transmute_core.swagger import (
    generate_swagger,
    get_swagger_static_root
)

STATIC_ROOT = "/_swagger/static"


def add_swagger(app, json_route, html_route):
    """
    a convenience method for both adding a swagger.json route,
    as well as adding a page showing the html documentation
    """
    app.route(json_route)(create_swagger_json_handler(app))
    add_swagger_api_route(app, html_route, json_route)


def add_swagger_api_route(app, target_route, swagger_json_route):
    """
    mount a swagger statics page.

    app: the aiohttp app object
    target_route: the path to mount the statics page.
    swagger_json_route: the path where the swagger json definitions is
        expected to be.
    """
    static_root = get_swagger_static_root()
    swagger_body = generate_swagger(
        STATIC_ROOT, swagger_json_route
    ).encode("utf-8")

    def swagger_ui():
        return Response(swagger_body, content_type="text/html")

    blueprint = Blueprint('swagger', __name__,
                          static_url_path=STATIC_ROOT,
                          static_folder=static_root)
    app.route(target_route)(swagger_ui)
    app.register_blueprint(blueprint)


def create_swagger_json_handler(app, title="example", version="1.0"):
    """
    Create a handler that returns the swagger definition
    for an application.

    This method assumes the application is using the
    TransmuteUrlDispatcher as the router.
    """

    spec = Swagger({
        "info": Info({"title": title, "version": version}),
        "paths": {},
        "swagger": "2.0",
        "basePath": "/",
    }).to_primitive()
    encoded_spec = json.dumps(spec).encode("UTF-8")

    def swagger():
        return Response(
            encoded_spec,
            # we allow CORS, so this can be requested at swagger.io
            headers={
                "Access-Control-Allow-Origin": "*"
            },
            content_type="application/json",
        )

    return swagger
