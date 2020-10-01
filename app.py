from flask import Flask, request, render_template
import re
import math

app = Flask("__name__")

q = ""

@app.route("/")
def loadPage():
	return render_template('index.html', query="")


@app.route("/", methods=['POST'])
def cosineSimilarity():
	

	universalSetOfUniqueWords = []
	matchPercentage = 0

	####################### Reference file #######################

	
	reference_file = request.form['reference_file']
	reference_file = reference_file.lower()

#Replace punctuation by space and split (REGEX)
	reference_fileWordList = re.sub("[^\w]", " ",reference_file).split()	

	for word in reference_fileWordList:
		if word not in universalSetOfUniqueWords:
			universalSetOfUniqueWords.append(word)

	########################### INPUT FILE #######################
 
	inputQuery = request.form['query']
	lowercaseQuery = inputQuery.lower()

#Replace punctuation by space and split (REGEX)
	queryWordList = re.sub("[^\w]", " ",lowercaseQuery).split()	

	for word in queryWordList:
		if word not in universalSetOfUniqueWords:
			universalSetOfUniqueWords.append(word)


	queryTF = []
	reference_fileTF = []

	for word in universalSetOfUniqueWords:
		queryTfCounter = 0
		reference_fileTfCounter = 0

		for word2 in queryWordList:
			if word == word2:
				queryTfCounter += 1
				
		queryTF.append(queryTfCounter)

		for word2 in reference_fileWordList:
			if word == word2:
				reference_fileTfCounter += 1
		reference_fileTF.append(reference_fileTfCounter)

	dotProduct = 0
	for i in range (len(queryTF)):
		dotProduct += queryTF[i]*reference_fileTF[i]

	queryVectorMagnitude = 0
	for i in range (len(queryTF)):
		queryVectorMagnitude += queryTF[i]**2
	queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

	reference_fileVectorMagnitude = 0
	for i in range (len(reference_fileTF)):
		reference_fileVectorMagnitude += reference_fileTF[i]**2
	reference_fileVectorMagnitude = math.sqrt(reference_fileVectorMagnitude)

	matchPercentage = (float)(dotProduct / (queryVectorMagnitude * reference_fileVectorMagnitude))*100

	
	print (queryWordList)
	print('\n')
	print (reference_fileWordList)
	
	'''
	print (queryTF)
	print('\n')
	print (reference_fileTF)
	'''

	output = "Input query text matches : %0.02f%% with reference file"%matchPercentage

	return render_template('index.html', query=inputQuery, output=output)

app.run(debug = True)
