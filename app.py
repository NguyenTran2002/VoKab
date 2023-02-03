# navigate to the Features folder
import sys
sys.path.append(sys.path[0]+'/./Features')

# UNIVERSAL IMPORT
from universal_imports import *

#------------------------------

# import all needed features
import helper
import grader

#------------------------------

app = flask.Flask(__name__, template_folder = 'Flask/templates', static_folder = 'Flask/static')

@app.route("/", methods=['GET', 'POST'])
def homepage():

    #--------------------------

    # temporarily hardcode the user
    user = "trann"

    # gets all study sets under the user
    study_sets = helper.get_study_sets(user)

    #--------------------------

    return flask.render_template("home.html", study_sets = study_sets)

@app.route("/writing_practice", methods = ['GET', 'POST'])
def writing_practice():

    # get the requested study set
    chosen_set = flask.request.form.get('set')

    #--------------------------

    return flask.render_template("writing_practice.html")

#------------------------------
@app.route("/writing_result", methods = ['GET', 'POST'])
def writing_result():

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