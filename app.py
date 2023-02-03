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

# initialize the Data Store object
data_store = helper.data_store()

#------------------------------

app = flask.Flask(__name__, template_folder = 'Flask/templates', static_folder = 'Flask/static')

@app.route("/", methods=['GET', 'POST'])
def homepage():

    #--------------------------

    # temporarily hardcode the user
    user = "trann"
    data_store.user = user

    # gets all study sets under the user
    study_sets = helper.get_study_sets(user) # list of strings

    # reformat all sets belonging to the user
    for set_name in study_sets:

        # path to the study set
        path = "Data/Users/" + user + "/" + set_name + ".csv"

        # read in the study set
        read_in_df = pd.read_csv(path, header = None)

        # check if the dataframe is already reformatted
        # get the number of columns of the dataframe
        num_cols = len(read_in_df.columns)

        # if the number of columns is 3, then it is already reformatted
        if num_cols >= 3:
            pass

        else:
            # reformat the dataframe
            set_df = helper.reformat_set_df(read_in_df)
            set_df.to_csv(path, index = False)

    #--------------------------

    """
    Note:
        - Information on drop down menu: https://stackoverflow.com/questions/66627718/how-to-grab-the-value-from-the-drop-down-menu-using-flask
    """

    return flask.render_template("home.html", study_sets = study_sets)

@app.route("/writing_practice_start", methods = ['GET', 'POST'])
def writing_practice_start():
    """
    DESCRIPTION:
        This is the first page of the writing practice feature.
        It will initialize the study set, shuffle the words, and ask the first words.
    """

    # get the requested study set
    chosen_set_name = flask.request.form.get('set')
    data_store.chosen_set_name = chosen_set_name

    # path to the set
    path = "Data/Users/" + data_store.user + "/" + chosen_set_name + ".csv"

    # read in the study set
    set_df = pd.read_csv(path)

    # generate an integer list of the length of the study set
    word_indices = list(range(len(set_df)))

    # shuffle the word indices
    study_indicies = word_indices
    random.shuffle(study_indicies)
    data_store.study_indicies = study_indicies

    # get the first word
    data_store.current_index = data_store.study_indicies.pop()

    # get the first definition
    first_definition = set_df.at[data_store.current_index, "Definition"]

    #--------------------------

    return flask.render_template("writing_practice.html", definition = first_definition)

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