from flask import Flask, request, jsonify, send_file, redirect, Response
from flask_restful import Resource, Api
import requests
import db
import navigatorHandlers
import os

# flask setup
app = Flask(__name__)
app.config.from_pyfile('../config.cfg')
# db setup
db = db.DB(os.environ['DYNAMO_DB_ENDPOINT'])

##########
## util ##
##########


def serveDocs():
    """Serves docs to browser"""
    return send_file("../api/index.html")


def errOut(code, error):
    """util function for returning non 2xx responses"""
    logging.error(error)
    return jsonify(code=code, error=error), code


#########
## api ##
#########

supportedCrudEndpoints = [{
    "name":
    "navigator",
    "path":
    "/navigator",
    "methods": [{
        "method": "GET",
        "handler": navigatorHandlers.getNavigator
    }, {
        "method": "POST",
        "handler": navigatorHandlers.postNavigator
    }, {
        "method": "PUT",
        "handler": navigatorHandlers.putNavigator
    }, {
        "method": "DELETE",
        "handler": navigatorHandlers.deleteNavigator
    }]
}]

for endpt in supportedCrudEndpoints:
    for m in endpt.get("methods"):
        app.add_url_rule(endpt.get("path"),
                         "{} a {}".format(m.get("method"), endpt.get("name")),
                         m.get("handler"),
                         methods=[m.get("method")])

# docs
app.add_url_rule('/', "swagger docs", serveDocs)

if __name__ == '__main__':
    app.run(debug=True)
