.. flask-transmute documentation master file, created by
   sphinx-quickstart on Wed Jun 17 09:23:47 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

flask-transmute
===============

A transmute framework for `flask <http://flask.pocoo.org/>`_. This framework provides:

* declarative generation of http handler interfaces by parsing function annotations
* validation and serialization to and from a variety of content types (e.g. json or yaml).
* validation and serialization to and from native python objects, using `schematics <http://schematics.readthedocs.org/en/latest/>`_.
* autodocumentation of all handlers generated this way, via `swagger <http://swagger.io/>`_.

flask-transmute is provided as a flask extension, and can be included in the
setup.py and/or requirements.txt for your service.

Here's a brief example::

    import flask_transmute
    from flask import Flask, Blueprint

    app = Flask(__name__)
    blueprint = Blueprint("blueprint", __name__, url_prefix="/foo")

    # creates an api that:
    # * accepts multiple markup types like json and yaml
    # * validates with input types that are specified
    @flask_transmute.route(app, paths='/multiple')
    # annotate types to tell flask-transmute what to verify
    # the type as (default string)
    @flask_transmute.annotate({"left": int, "right": int, "return": int})
    def multiply(left, right):
        return left * right

    # if you use python 3.5+, you can annotate directly
    # in the method signature.
    @flask_transmute.route(app, paths='/multiply3')
    def multiply_3(left: int, right: int) -> int:
        return left + right

    # blueprints are supported as well
    @flask_transmute.route(blueprint, paths='/subroute')
    @flask_transmute.annotate({"return": bool})
    def subroute():
        return True

    app.register_blueprint(blueprint)

    # finally, you can add a swagger json and a documentation page by:
    flask_transmute.add_swagger(app, "/swagger.json", "/swagger")

    app.run()

---------------------
Legacy Implementation
---------------------

flask-transmute 1.0 uses a completely different implementation of the
transmute functionality based on `transmute-core
<http://transmute-core.readthedocs.io/>`_

Documentation for the pre-1.0 version can be found under the legacy section.



Contents:

.. toctree::
   :maxdepth: 2

   install
   routes
   serialization
   documentation
   legacy/index.rst
