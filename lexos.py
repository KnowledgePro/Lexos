#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
from urllib import unquote
from os.path import join as pathjoin

from flask import Flask, redirect, render_template, request, session, url_for, send_file

import helpers.general_functions as general_functions
from managers.file_manager import FileManager
import managers.session_manager as session_functions
import helpers.constants as constants
from managers import utility






# ------------
import managers.utility

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = constants.MAX_FILE_SIZE  # convert into byte


@app.route("/", methods=["GET"])  # Tells Flask to load this function when someone is at '/'
def base():
    """
    Page behavior for the base url ('/') of the site. Handles redirection to other pages.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    try:
        if not os.path.isdir(os.path.join(constants.UPLOAD_FOLDER, session['id'])):
            session_functions.init()  # Check browser for recent Lexos session
    except:
        if 'id' not in session:  # If session was never generated
            session_functions.init()  # Initialize the session if needed

    return redirect(url_for('upload'))


@app.route("/downloadworkspace",
           methods=["GET"])  # Tells Flask to load this function when someone is at '/downloadworkspace'
def downloadworkspace():
    """
    Downloads workspace that stores all the session contents, which can be uploaded and restore all the workspace.
    """
    fileManager = managers.utility.loadFileManager()
    path = fileManager.zipWorkSpace()

    return send_file(path, attachment_filename=constants.WORKSPACE_FILENAME, as_attachment=True)


@app.route("/reset", methods=["GET"])  # Tells Flask to load this function when someone is at '/reset'
def reset():
    """
    Resets the session and initializes a new one every time the reset URL is used
    (either manually or via the "Reset" button)
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    session_functions.reset()  # Reset the session and session folder
    session_functions.init()  # Initialize the new session

    # initialize the file manager
    emptyFileManager = FileManager()

    utility.saveFileManager(emptyFileManager)
    return redirect(url_for('upload'))


@app.route("/upload", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/upload'
def upload():
    """
    Handles the functionality of the upload page. It uploads files to be used
    in the current session.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    if request.method == "GET":
        return render_template('upload.html', MAX_FILE_SIZE=constants.MAX_FILE_SIZE,
                               MAX_FILE_SIZE_INT=constants.MAX_FILE_SIZE_INT,
                               MAX_FILE_SIZE_UNITS=constants.MAX_FILE_SIZE_UNITS)

    if 'X_FILENAME' in request.headers:  # X_FILENAME is the flag to signify a file upload
        # File upload through javascript
        fileManager = managers.utility.loadFileManager()

        # --- check file name ---
        fileName = request.headers[
            'X_FILENAME']  # Grab the filename, which will be UTF-8 percent-encoded (e.g. '%E7' instead of python's '\xe7')
        if isinstance(fileName, unicode):  # If the filename comes through as unicode
            fileName = fileName.encode('ascii')  # Convert to an ascii string
        fileName = unquote(fileName).decode(
            'utf-8')  # Unquote using urllib's percent-encoding decoder (turns '%E7' into '\xe7'), then deocde it
        # --- end check file name ---

        if fileName.endswith('.lexos'):
            fileManager.handleUploadWorkSpace()

            # update filemanager
            fileManager = managers.utility.loadFileManager()
            fileManager.updateWorkspace()

        else:
            fileManager.addUploadFile(request.data, fileName)

        managers.utility.saveFileManager(fileManager)
        return 'success'


@app.route("/select_old", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/select_old'
def select_old():
    """
    Handles the functionality of the select page. Its primary role is to activate/deactivate
    specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()  # Usual loading of the FileManager

    if request.method == "GET":
        activePreviews = fileManager.getPreviewsOfActive()
        inactivePreviews = fileManager.getPreviewsOfInactive()

        return render_template('select_old.html', activeFiles=activePreviews, inactiveFiles=inactivePreviews)

    if 'toggleFile' in request.headers:
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        fileID = int(request.data)

        fileManager.toggleFile(fileID)  # Toggle the file from active to inactive or vice versa

    elif 'setLabel' in request.headers:
        newLabel = (request.headers['setLabel']).decode('utf-8')
        fileID = int(request.data)

        fileManager.files[fileID].label = newLabel

    elif 'disableAll' in request.headers:
        fileManager.disableAll()

    elif 'selectAll' in request.headers:
        fileManager.enableAll()

    elif 'applyClassLabel' in request.headers:
        fileManager.classifyActiveFiles()

    elif 'deleteActive' in request.headers:
        fileManager.deleteActiveFiles()

    managers.utility.saveFileManager(fileManager)

    return ''  # Return an empty string because you have to return something


@app.route("/scrub", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/scrub'
def scrub():
    """
    Handles the functionality of the scrub page. It scrubs the files depending on the
    specifications chosen by the user, with an option to download the scrubbed files.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'scrubbingoptions' not in session:
            session['scrubbingoptions'] = constants.DEFAULT_SCRUB_OPTIONS

        previews = fileManager.getPreviewsOfActive()
        tagsPresent, DOEPresent = fileManager.checkActivesTags()

        return render_template('scrub.html', previews=previews, haveTags=tagsPresent, haveDOE=DOEPresent)

    if 'preview' in request.form or 'apply' in request.form:
        # The 'Preview Scrubbing' or 'Apply Scrubbing' button is clicked on scrub.html.
        session_functions.cacheAlterationFiles()
        session_functions.cacheScrubOptions()

        # saves changes only if 'Apply Scrubbing' button is clicked
        savingChanges = True if 'apply' in request.form else False

        previews = fileManager.scrubFiles(savingChanges=savingChanges)
        tagsPresent, DOEPresent = fileManager.checkActivesTags()

        if savingChanges:
            managers.utility.saveFileManager(fileManager)

        return render_template('scrub.html', previews=previews, haveTags=tagsPresent, haveDOE=DOEPresent)

    if 'download' in request.form:
        # The 'Download Scrubbed Files' button is clicked on scrub.html.
        # sends zipped files to downloads folder.
        return fileManager.zipActiveFiles('scrubbed.zip')


@app.route("/cut", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/cut'
def cut():
    """
    Handles the functionality of the cut page. It cuts the files into various segments
    depending on the specifications chosen by the user, and sends the text segments.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cuttingoptions' not in session:
            session['cuttingoptions'] = constants.DEFAULT_CUT_OPTIONS

        previews = fileManager.getPreviewsOfActive()

        return render_template('cut.html', previews=previews, num_active_files=len(previews))

    if 'preview' in request.form or 'apply' in request.form:

        # The 'Preview Cuts' or 'Apply Cuts' button is clicked on cut.html.
        session_functions.cacheCuttingOptions()

        savingChanges = True if 'apply' in request.form else False  # Saving changes only if apply in request form
        previews = fileManager.cutFiles(savingChanges=savingChanges)

        if savingChanges:
            managers.utility.saveFileManager(fileManager)

        return render_template('cut.html', previews=previews, num_active_files=len(previews))

    if 'downloadchunks' in request.form:
        # The 'Download Segmented Files' button is clicked on cut.html
        # sends zipped files to downloads folder
        return fileManager.zipActiveFiles('cut_files.zip')


@app.route("/tokenizer", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/tokenize'
def tokenizer():
    """
    Handles the functionality on the tokenizer page. It analyzes the texts to produce
    and send various frequency matrices.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()

    if request.method == "GET":
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
        if 'csvoptions' not in session:
            session['csvoptions'] = constants.DEFAULT_CSV_OPTIONS
        # "GET" request occurs when the page is first loaded.
        labels = fileManager.getActiveLabels()
        return render_template('tokenizer.html', labels=labels, matrixExist=False)

    if 'gen-csv' in request.form:
        # The 'Generate and Visualize Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        labels = fileManager.getActiveLabels()

        matrixTitle, tableStr = utility.generateTokenizeResults(fileManager)
        managers.utility.saveFileManager(fileManager)

        return render_template('tokenizer.html', labels=labels, matrixTitle=matrixTitle,
                               tableStr=tableStr, matrixExist=True)

    if 'get-csv' in request.form:
        # The 'Download Matrix' button is clicked on tokenizer.html.
        session_functions.cacheAnalysisOption()
        session_functions.cacheCSVOptions()
        savePath, fileExtension = utility.generateCSV(fileManager)
        managers.utility.saveFileManager(fileManager)

        return send_file(savePath, attachment_filename="frequency_matrix" + fileExtension, as_attachment=True)


@app.route("/statistics",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/statsgenerator'
def statistics():
    """
    Handles the functionality on the Statistics page ...
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
        if 'statisticoption' not in session:
            session['statisticoption'] = {'segmentlist': map(unicode, labels.keys())}  # default is all on

        return render_template('statistics.html', labels=labels, labels2=labels)

    if request.method == "POST":

        FileInfoDict, corpusInfoDict = utility.generateStatistics(fileManager)

        session_functions.cacheAnalysisOption()
        session_functions.cacheStatisticOption()
        # DO NOT save fileManager!
        return render_template('statistics.html', labels=labels, FileInfoDict=FileInfoDict,
                               corpusInfoDict=corpusInfoDict)


# @app.route("/statisticsimage",
#            methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/statistics'
# def statisticsimage():
#     """
#     Reads the png image of the corpus statistics and displays it on the web browser.
#     Note: Returns a response object with the statistics png to flask and eventually to the browser.
#     """
#     imagePath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER,
#                          constants.CORPUS_INFORMATION_FIGNAME)
#     return send_file(imagePath)


@app.route("/hierarchy", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/hierarchy'
def hierarchy():
    """
    Handles the functionality on the hierarchy page. It analyzes the various texts and
    displays a dendrogram.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()
    leq = '≤'.decode('utf-8')

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = fileManager.getActiveLabels()
        thresholdOps = {}
        return render_template('hierarchy.html', labels=labels, thresholdOps=thresholdOps)

    if 'dendro_download' in request.form:
        # The 'Download Dendrogram' button is clicked on hierarchy.html.
        # sends pdf file to downloads folder.
        utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".pdf" if request.form['title'] != '' else 'dendrogram.pdf'
        session_functions.cacheAnalysisOption()
        session_functions.cacheHierarchyOption()
        return send_file(pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER + "dendrogram.pdf"),
                         attachment_filename=attachmentname, as_attachment=True)

    if 'dendroSVG_download' in request.form:
        utility.generateDendrogram(fileManager)
        attachmentname = "den_" + request.form['title'] + ".svg" if request.form['title'] != '' else 'dendrogram.svg'
        session_functions.cacheAnalysisOption()
        session_functions.cacheHierarchyOption()
        return send_file(pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER + "dendrogram.svg"),
                         attachment_filename=attachmentname, as_attachment=True)

    if 'getdendro' in request.form:
        # The 'Get Dendrogram' button is clicked on hierarchy.html.

        pdfPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold = utility.generateDendrogram(
            fileManager)
        session['dengenerated'] = True
        labels = fileManager.getActiveLabels()

        inconsistentOp = "0 " + leq + " t " + leq + " " + str(inconsistentMax)
        maxclustOp = "2 " + leq + " t " + leq + " " + str(maxclustMax)
        distanceOp = str(distanceMin) + " " + leq + " t " + leq + " " + str(distanceMax)
        monocritOp = str(monocritMin) + " " + leq + " t " + leq + " " + str(monocritMax)

        thresholdOps = {"inconsistent": inconsistentOp, "maxclust": maxclustOp, "distance": distanceOp,
                        "monocrit": monocritOp}

        managers.utility.saveFileManager(fileManager)
        session_functions.cacheAnalysisOption()
        session_functions.cacheHierarchyOption()
        return render_template('hierarchy.html', labels=labels, pdfPageNumber=pdfPageNumber, score=score,
                               inconsistentMax=inconsistentMax, maxclustMax=maxclustMax, distanceMax=distanceMax,
                               distanceMin=distanceMin, monocritMax=monocritMax, monocritMin=monocritMin,
                               threshold=threshold, thresholdOps=thresholdOps)


@app.route("/dendrogramimage",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/dendrogramimage'
def dendrogramimage():
    """
    Reads the png image of the dendrogram and displays it on the web browser.
    *dendrogramimage() linked to in analysis.html, displaying the dendrogram.png
    Note: Returns a response object with the dendrogram png to flask and eventually to the browser.
    """
    # dendrogramimage() is called in analysis.html, displaying the dendrogram.png (if session['dengenerated'] != False).
    imagePath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER, constants.DENDROGRAM_FILENAME)
    return send_file(imagePath)


@app.route("/kmeans", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/kmeans'
def kmeans():
    """
    Handles the functionality on the kmeans page. It analyzes the various texts and
    displays the class label of the files.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()
    defaultK = int(len(labels) / 2)

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
        if 'kmeanoption' not in session:
            session['kmeanoption'] = constants.DEFAULT_KMEAN_OPTIONS

        return render_template('kmeans.html', labels=labels, silhouettescore='', kmeansIndex=[], fileNameStr='',
                               fileNumber=len(labels), KValue=0, defaultK=defaultK,
                               colorChartStr='', kmeansdatagenerated=False)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')


        if request.form['viz'] == 'PCA':
            kmeansIndex, silhouetteScore, fileNameStr, KValue, colorChartStr = utility.generateKMeansPCA(fileManager)

            session_functions.cacheAnalysisOption()
            session_functions.cacheKmeanOption()
            managers.utility.saveFileManager(fileManager)
            return render_template('kmeans.html', labels=labels, silhouettescore=silhouetteScore,
                                   kmeansIndex=kmeansIndex,
                                   fileNameStr=fileNameStr, fileNumber=len(labels), KValue=KValue, defaultK=defaultK,
                                   colorChartStr=colorChartStr, kmeansdatagenerated=True)

        elif request.form['viz'] == 'Voronoi':

            kmeansIndex, silhouetteScore, fileNameStr, KValue, colorChartStr, finalPointsList, finalCentroidsList, textData, maxVal = utility.generateKMeansVoronoi(
                fileManager)

            session_functions.cacheAnalysisOption()
            session_functions.cacheKmeanOption()
            managers.utility.saveFileManager(fileManager)
            return render_template('kmeans.html', labels=labels, silhouettescore=silhouetteScore,
                                   kmeansIndex=kmeansIndex, fileNameStr=fileNameStr, fileNumber=len(labels),
                                   KValue=KValue, defaultK=defaultK, colorChartStr=colorChartStr,
                                   finalPointsList=finalPointsList, finalCentroidsList=finalCentroidsList,
                                   textData=textData, maxVal=maxVal, kmeansdatagenerated=True)


@app.route("/kmeansimage",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/kmeansimage'
def kmeansimage():
    """
    Reads the png image of the kmeans and displays it on the web browser.

    *kmeansimage() linked to in analysis.html, displaying the kmeansimage.png

    Note: Returns a response object with the kmeansimage png to flask and eventually to the browser.
    """
    # kmeansimage() is called in kmeans.html, displaying the KMEANS_GRAPH_FILENAME (if session['kmeansdatagenerated'] != False).
    imagePath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER, constants.KMEANS_GRAPH_FILENAME)
    return send_file(imagePath)


@app.route("/rollingwindow",
           methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/rollingwindow'
def rollingwindow():
    """
    Handles the functionality on the rollingwindow page. It analyzes the various
    texts using a rolling window of analysis.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'rwoption' not in session:
            session['rwoption'] = constants.DEFAULT_ROLLINGWINDOW_OPTIONS

        # default legendlabels
        legendLabels = [""]

        return render_template('rwanalysis.html', labels=labels, legendLabels=legendLabels,
                               rwadatagenerated=False)

    if request.method == "POST":
        # "POST" request occurs when user hits submit (Get Graph) button

        dataPoints, dataList, graphTitle, xAxisLabel, yAxisLabel, legendLabels = utility.generateRWA(fileManager)

        if 'get-RW-plot' in request.form:
            # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.

            savePath, fileExtension = utility.generateRWmatrixPlot(dataPoints, legendLabels)

            return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        if 'get-RW-data' in request.form:
            # The 'Generate and Download Matrix' button is clicked on rollingwindow.html.

            savePath, fileExtension = utility.generateRWmatrix(dataList)

            return send_file(savePath, attachment_filename="rollingwindow_matrix" + fileExtension, as_attachment=True)

        session_functions.cacheRWAnalysisOption()
        return render_template('rwanalysis.html', labels=labels,
                               data=dataPoints,
                               graphTitle=graphTitle,
                               xAxisLabel=xAxisLabel,
                               yAxisLabel=yAxisLabel,
                               legendLabels=legendLabels,
                               rwadatagenerated=True)


@app.route("/wordcloud", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/wordcloud'
def wordcloud():
    """
    Handles the functionality on the visualisation page -- a prototype for displaying
    single word cloud graphs.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS

        # there is no wordcloud option so we don't initialize that
        return render_template('wordcloud.html', labels=labels)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        JSONObj = utility.generateJSONForD3(fileManager, mergedSet=True)

        # Create a list of column values for the word count table
        from operator import itemgetter

        terms = sorted(JSONObj["children"], key=itemgetter('size'), reverse=True)

        columnValues = []

        for term in terms:
            rows = [term["name"], term["size"]]
            columnValues.append(rows)

        session_functions.cacheCloudOption()
        return render_template('wordcloud.html', labels=labels, JSONObj=JSONObj, columnValues=columnValues)


@app.route("/multicloud", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/multicloud'
def multicloud():
    """
    Handles the functionality on the multicloud pages.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """

    fileManager = managers.utility.loadFileManager()

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'multicloudoptions' not in session:
            session['multicloudoptions'] = constants.DEFAULT_MULTICLOUD_OPTIONS

        labels = fileManager.getActiveLabels()

        return render_template('multicloud.html', jsonStr="", labels=labels)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        labels = fileManager.getActiveLabels()
        JSONObj = utility.generateMCJSONObj(fileManager)

        session_functions.cacheCloudOption()
        session_functions.cacheMultiCloudOptions()
#        return render_template('multicloud.html', JSONObj=JSONObj, labels=labels, loading='loading')
        return render_template('multicloud.html', JSONObj=JSONObj, labels=labels)


@app.route("/viz", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/viz'
def viz():
    """
    Handles the functionality on the alternate bubbleViz page with performance improvements.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    fileManager = managers.utility.loadFileManager()

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'cloudoption' not in session:
            session['cloudoption'] = constants.DEFAULT_CLOUD_OPTIONS
        if 'bubblevisoption' not in session:
            session['bubblevisoption'] = constants.DEFAULT_BUBBLEVIZ_OPTIONS

        labels = fileManager.getActiveLabels()

        return render_template('viz.html', JSONObj="", labels=labels)

    if request.method == "POST":
        # "POST" request occur when html form is submitted (i.e. 'Get Dendrogram', 'Download...')
        labels = fileManager.getActiveLabels()
        JSONObj = utility.generateJSONForD3(fileManager, mergedSet=True)

        session_functions.cacheCloudOption()
        session_functions.cacheBubbleVizOption()
#        return render_template('viz.html', JSONObj=JSONObj, labels=labels, loading='loading')
        return render_template('viz.html', JSONObj=JSONObj, labels=labels)

@app.route("/extension", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/extension'
def extension():
    """
    Handles the functionality on the External Tools page -- a prototype for displaying
    possible external analysis options.
    Note: Returns a response object (often a render_template call) to flask and eventually
    to the browser.
    """
    return render_template('extension.html')


@app.route("/similarity", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/extension'
def similarity():
    """
    Handles the similarity query page functionality. Returns ranked list of files and their cosine similarities to a comparison document.
    """

    fileManager = managers.utility.loadFileManager()
    labels = {}
    oldLabel = fileManager.getActiveLabels()
    for i in oldLabel:
        labels[str(i)] = oldLabel[i].encode("utf-8");
    print labels

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
        if 'uploadname' not in session:
            session['similarities'] = constants.DEFAULT_SIM_OPTIONS

        return render_template('similarity.html', labels=labels, docsListScore="", docsListName="",
                               similaritiesgenerated=False)

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        docsListScore, docsListName = utility.generateSimilarities(fileManager)

        session_functions.cacheAnalysisOption()
        session_functions.cacheSimOptions()
        return render_template('similarity.html', labels=labels, docsListScore=docsListScore, docsListName=docsListName,
                               similaritiesgenerated=True)


@app.route("/topword", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/topword'
def topword():
    """
    Handles the topword page functionality.
    """
    fileManager = managers.utility.loadFileManager()
    labels = fileManager.getActiveLabels()

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded

        if 'topwordoption' not in session:
            session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS

        # get the class label and eliminate the id (this is not the unique id in filemanager)
        ClassdivisionMap = fileManager.getClassDivisionMap()[1:]

        # if there is no file active (ClassdivisionMap == []) just jump to the page
        # notice python eval from right to left
        # if there is only one chunk then make the default test prop-z for all
        if ClassdivisionMap != [] and len(ClassdivisionMap[0]) == 1:
            session['topwordoption']['testMethodType'] = 'pz'
            session['topwordoption']['testInput'] = 'useAll'

        return render_template('topword.html', labels=labels, classmap=ClassdivisionMap, topwordsgenerated='class_div')

    if request.method == "POST":
        # 'POST' request occur when html form is submitted (i.e. 'Get Graphs', 'Download...')
        if request.form['testMethodType'] == 'pz':
            if request.form['testInput'] == 'useclass':  # prop-z test for class

                result = utility.GenerateZTestTopWord(fileManager)  # get the topword test result

                if 'get-topword' in request.form:  # download topword
                    path = utility.getTopWordCSV(result, 'pzClass')

                    session_functions.cacheAnalysisOption()
                    session_functions.cacheTopwordOptions()
                    return send_file(path, attachment_filename=constants.TOPWORD_CSV_FILE_NAME, as_attachment=True)

                else:
                    # only give the user a preview of the topWord
                    for key in result.keys():
                        if len(result[key]) > 20:
                            result.update({key: result[key][:20]})

                    session_functions.cacheAnalysisOption()
                    session_functions.cacheTopwordOptions()
                    return render_template('topword.html', result=result, labels=labels, topwordsgenerated='pz_class')

            else:  # prop-z test for all

                result = utility.GenerateZTestTopWord(fileManager) # get the topword test result

                if 'get-topword' in request.form:  # download topword
                    path = utility.getTopWordCSV(result, 'pzAll')

                    session_functions.cacheAnalysisOption()
                    session_functions.cacheTopwordOptions()
                    return send_file(path, attachment_filename=constants.TOPWORD_CSV_FILE_NAME, as_attachment=True)

                else:
                    # only give the user a preview of the topWord
                    for i in range(len(result)):
                        if len(result[i][1]) > 20:
                            result[i][1] = result[i][1][:20]

                    session_functions.cacheAnalysisOption()
                    session_functions.cacheTopwordOptions()
                    return render_template('topword.html', result=result, labels=labels, topwordsgenerated='pz_all')

        else:  # Kruskal-Wallis test

            result = utility.generateKWTopwords(fileManager) # get the topword test result

            if 'get-topword' in request.form:  # download topword
                path = utility.getTopWordCSV(result, 'KW')

                session_functions.cacheAnalysisOption()
                session_functions.cacheTopwordOptions()
                return send_file(path, attachment_filename=constants.TOPWORD_CSV_FILE_NAME, as_attachment=True)

            else:
                # only give the user a preview of the topWord
                result = result[:50] if len(result) > 50 else result

                session_functions.cacheAnalysisOption()
                session_functions.cacheTopwordOptions()
                return render_template('topword.html', result=result, labels=labels, topwordsgenerated='KW')


# =================== Helpful functions ===================

def install_secret_key(fileName='secret_key'):
    """
    Creates an encryption key for a secure session.
    Args:
        fileName: A string representing the secret key.
    Returns:
        None
    """
    fileName = os.path.join(app.static_folder, fileName)
    try:
        app.config['SECRET_KEY'] = open(fileName, 'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        if not os.path.isdir(os.path.dirname(fileName)):
            print 'mkdir -p', os.path.dirname(fileName)
        print 'head -c 24 /dev/urandom >', fileName
        sys.exit(1)


# ================ End of Helpful functions ===============

# =========== Temporary development functions =============
@app.route("/select", methods=["GET", "POST"])  # Tells Flask to load this function when someone is at '/select'
def select():
    """
    Handles the functionality of the select page. Its primary role is to activate/deactivate
    specific files depending on the user's input.
    Note: Returns a response object (often a render_template call) to flask and eventually
          to the browser.
    """
    fileManager = managers.utility.loadFileManager()  # Usual loading of the FileManager

    if request.method == "GET":

        rows = fileManager.getPreviewsOfAll()
        for row in rows:
            if row["state"] == True:
                row["state"] = "ui-selected"
            else:
                row["state"] = ""

        return render_template('select.html', rows=rows, itm="best-practices")

    if 'previewTest' in request.headers:
        fileID = int(request.data)
        fileLabel = fileManager.files[fileID].label
        filePreview = fileManager.files[fileID].getPreview()
        previewVals = {"id": fileID, "label": fileLabel, "previewText": filePreview}
        import json

        return json.dumps(previewVals)

    if 'toggleFile' in request.headers:
        # Catch-all for any POST request.
        # On the select page, POSTs come from JavaScript AJAX XHRequests.
        fileID = int(request.data)

        fileManager.toggleFile(fileID)  # Toggle the file from active to inactive or vice versa

    elif 'toggliFy' in request.headers:
        fileIDs = request.data
        fileIDs = fileIDs.split(",")
        fileManager.disableAll()

        fileManager.togglify(fileIDs)  # Toggle the file from active to inactive or vice versa

    elif 'setLabel' in request.headers:
        newName = (request.headers['setLabel']).decode('utf-8')
        fileID = int(request.data)

        fileManager.files[fileID].setName(newName)
        fileManager.files[fileID].label = newName

    elif 'setClass' in request.headers:
        newClassLabel = (request.headers['setClass']).decode('utf-8')
        fileID = int(request.data)
        fileManager.files[fileID].setClassLabel(newClassLabel)

    elif 'disableAll' in request.headers:
        fileManager.disableAll()

    elif 'selectAll' in request.headers:
        fileManager.enableAll()

    elif 'applyClassLabel' in request.headers:
        fileManager.classifyActiveFiles()

    elif 'deleteActive' in request.headers:
        fileManager.deleteActiveFiles()

    elif 'deleteRow' in request.headers:
        fileManager.deleteFiles(request.form.keys())  # delete the file in request.form

    managers.utility.saveFileManager(fileManager)
    return ''  # Return an empty string because you have to return something

# ======= End of temporary development functions ======= #

install_secret_key()
app.debug = True
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = unicode
app.jinja_env.filters['time'] = time.time()
app.jinja_env.filters['natsort'] = general_functions.natsort

# app.config['PROFILE'] = True
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [300])

if __name__ == '__main__':
    app.run()
