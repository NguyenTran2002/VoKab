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
    """
    DESCRIPTION:
        Homepage of the website.
        These are what's going on:
            1. get the user who's studying
            2. check all study sets under the user
            3. reformat the sets if needed
    """

    #--------------------------

    # temporarily hardcode the user
    user = "chenk"
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

#------------------------------

@app.route("/writing_practice_start", methods = ['GET', 'POST'])
def writing_practice_start():
    """
    DESCRIPTION:
        This is the first page of the writing practice feature.
        It will initialize the study set, shuffle the words, and ask the first words.
        These are what's going on:
            1. get the study set that the user wants to study
            2. read in the set from local storage
            3. shuffle the set and stored the shuffled order in data_store
            4. get the first word and definition
            5. ask the first word, then redirect to the check result page
    """

    # get the requested study set
    chosen_set_name = flask.request.form.get('set')
    data_store.chosen_set_name = chosen_set_name

    # path to the set
    path = "Data/Users/" + data_store.user + "/" + chosen_set_name + ".csv"
    data_store.set_path = path

    # read in the study set
    set_df = pd.read_csv(path)
    data_store.set_df = set_df
    data_store.to_export_df = set_df.copy()

    # filter the set to only contains words with mastery level < 3 (not mastered)
    not_mastered_df = set_df[set_df['Mastery'] < 3]
    word_indices = list(not_mastered_df.index.values)

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

@app.route("/writing_practice", methods = ['GET', 'POST'])
def writing_practice():
    """
    DESCRIPTION:
        This is a subsequent page of the writing practice feature.
        These are what's going on:
            1. get the next word and definition
            2. ask the next word
            3. redirect to the check result page
    """

    # if the study set round is completed, update the data, and redirect to the completed page
    if len(data_store.study_indicies) == 0:

        # the final dataframe
        final_df = data_store.to_export_df.copy()

        # path
        path = data_store.set_path

        # DEBUGGING
        print(path)
        
        # export the dataframe
        final_df.to_csv(path, index = False)

        # update the set_df object
        data_store.set_df = final_df

        return flask.render_template("set_completed.html")

    else:

        # get the next word
        data_store.current_index = data_store.study_indicies.pop()

        # get the next definition
        definition = data_store.set_df.at[data_store.current_index, "Definition"]

        #--------------------------

        return flask.render_template("writing_practice.html", definition = definition)

#------------------------------

@app.route("/writing_result", methods = ['GET'])
def writing_result():
    """
    DESCRIPTION:
        This is the page that checks the user's answer.
        These are what's going on:
            1. get the user's answer
            2. get the correct answer
            3. compare the two answers, and display whether the user is correct or not
    """

    # get the user's answer
    user_answer = flask.request.args.get('user_answer')

    # dataframe information
    set_df = data_store.set_df
    current_index = data_store.current_index

    # print(helper.data_store.set_df.at[helper.data_store.current_index, "Word"])

    # get the correct answer
    result = grader.check_answer(user_answer, set_df, current_index)

    # if the answer is correct
    if result == True:

        # to export df
        to_export_df = data_store.to_export_df

        # update the data of the result
        to_export_df = helper.update_data_after_answer(result, to_export_df, current_index)

        data_store.to_export_df = to_export_df

        # render webpage
        return flask.render_template("writing_result_correct.html")

    else:

        # to export df
        to_export_df = data_store.to_export_df

        # update the data of the result
        to_export_df = helper.update_data_after_answer(False, to_export_df, current_index)

        data_store.to_export_df = to_export_df

        # render webpage
        return flask.render_template("writing_result_wrong.html",\
            user_answer = user_answer,\
            correct_answer = result) 

#------------------------------

@app.route("/learning_progress", methods = ['GET'])
def learning_progress():

    """
    DESCRIPTION:
        Show the user the learning progress on a particular study set.
    """

    # get the requested study set
    chosen_set_name = flask.request.args.get('set')
    data_store.chosen_set_name = chosen_set_name

    # path to the set
    path = "Data/Users/" + data_store.user + "/" + chosen_set_name + ".csv"
    data_store.set_path = path

    # read in the study set
    set_df = pd.read_csv(path)
    data_store.set_df = set_df

    # sort by mastery level
    set_df = set_df.sort_values(by = ['Mastery'], ascending = False)

    # filter the set to only contains words with certain conditions
    mastered_df = set_df[set_df['Mastery'] == 3]
    learning_df = set_df[(set_df['Mastery'] == 1) | (set_df['Mastery'] == 2)]
    not_learned_df = set_df[set_df['Mastery'] == 0]
    
    # get the metrics
    num_mastered = len(mastered_df)
    num_learning = len(learning_df)
    num_not_learned = len(not_learned_df)
    num_set = len(set_df)

    # calculate the percentage of words mastered, rounded to the nearest integer
    percent_mastered = round(num_mastered / num_set * 100)

    #--------------------------

    return flask.render_template("learning_progress.html",\
        study_set = chosen_set_name,\
        num_mastered = num_mastered,\
        num_learning = num_learning,\
        num_not_learned = num_not_learned,\
        num_set = num_set,\
        percent_mastered = percent_mastered,\
        study_set_html = [set_df.to_html(classes = 'study_set', header = "true")])

#------------------------------

@app.route("/reset_progress", methods = ['GET'])
def reset_progress():

    """
    DESCRIPTION:
        Reset the mastery level of all words in the study set
    """

    # get the requested study set
    chosen_set_name = data_store.chosen_set_name\

    # path to the set
    path = data_store.set_path

    # read in the study set
    set_df = pd.read_csv(path)
    data_store.set_df = set_df

    # reset the mastery level
    set_df['Mastery'] = 0

    # export the dataframe
    set_df.to_csv(path, index = False)
    data_store.set_df = set_df

    # sort by mastery level
    set_df = set_df.sort_values(by = ['Mastery'], ascending = False)

    # filter the set to only contains words with certain conditions
    mastered_df = set_df[set_df['Mastery'] == 3]
    learning_df = set_df[(set_df['Mastery'] == 1) | (set_df['Mastery'] == 2)]
    not_learned_df = set_df[set_df['Mastery'] == 0]
    
    # get the metrics
    num_mastered = len(mastered_df)
    num_learning = len(learning_df)
    num_not_learned = len(not_learned_df)
    num_set = len(set_df)

    # calculate the percentage of words mastered, rounded to the nearest integer
    percent_mastered = round(num_mastered / num_set * 100)

    #--------------------------

    return flask.render_template("reset_progress.html",\
        study_set = chosen_set_name,\
        num_mastered = num_mastered,\
        num_learning = num_learning,\
        num_not_learned = num_not_learned,\
        num_set = num_set,\
        percent_mastered = percent_mastered,\
        study_set_html = [set_df.to_html(classes = 'study_set', header = "true")])

#------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template("404_page.html")

#------------------------------
@app.errorhandler(500)
def page_not_found(e):
    return flask.render_template("500_page.html")

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