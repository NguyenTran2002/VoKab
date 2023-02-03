# navigate to the Features folder
import sys
sys.path.append(sys.path[0]+'/./Features')

# UNIVERSAL IMPORT
from universal_imports import *

#------------------------------

app = flask.Flask(__name__, template_folder = 'Flask/templates', static_folder = 'Flask/static')

@app.route("/")
def homepage():

    #--------------------------

    # check if there is any new transactions added to our mint.csv data

    #--------------------------

    return flask.render_template("home.html")

@app.route("/writing_practice")
def writing_practice():

    #--------------------------

    # start writing practice right away

    #--------------------------

    return flask.render_template("writing_practice.html")

#------------------------------
@app.route("/writing_result")
def writing_result():

    #--------------------------

    # start writing practice right away

    #--------------------------

    return flask.render_template("writing_result.html")

#------------------------------
if __name__ == '__main__':

    app.run(port = 2700)

    # import logging
    # logging.basicConfig(filename='error.txt',level=logging.DEBUG)

    """
    TO IMPLEMENT
    - output the graph to EVERY SINGLE FOLDER (not only the static folder)
    - test which folder output the damn graph
    """