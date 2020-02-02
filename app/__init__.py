from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
import gkeepapi

import nltk
import sklearn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

account = {
	'user': 'introspecthack@gmail.com',
	'password': 'Kyjus2020',
}

vectorizer = TfidfVectorizer()
def trainModel(notes):
	corpus = []
	for note in notes:
		corpus.append(note.text) 
	model = vectorizer.fit_transform(corpus)
	return vectorizer.get_feature_names(), model	# also returns model

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
sid = SentimentIntensityAnalyzer()

def calcScore(text):
	return sid.polarity_scores(text)

# get a rank of all the keywords depending on their intersections
# update: using bigrams to see an improvement in contexts over POS tagging
def getKeyWords(corpus, positive=True):
	# step 0: score every note depending on the analysis
	score = [[calcScore(note.text), note.text] for note in corpus]
	# step 1: get all of the notes of a specific compound category
	if positive == True:
		texts = [d for d in sorted(score, key=lambda item: item[0]['compound']) if d[0]['compound'] > 0]
	else:
		texts = [d for d in sorted(score, key=lambda item: item[0]['compound']) if d[0]['compound'] < 0]
	# step 2: rank every token in the arrays depending on how common they are...
	# step 2.1: tokenize each text and then bigram them
	# step 2.2: then find intersects and rank accordingly
	bigrammed_texts = []
	for text in texts:
		bigrammed_texts.append([d for d in nltk.bigrams(nltk.word_tokenize(text[1]))])

	# We do not need a POS tagger here, since we are trying bigrams.
	# word_filter = ['Mr.', 'Mrs.', 'i', 'Dr.']
	# pos_filter = ['NN', 'NNP', 'NNPS', 'NNS']
	ranked_tokens = {}
	for text in bigrammed_texts:
		for bigram in text:
			# if token[1] in pos_filter and token[0] not in word_filter:
			if bigram in ranked_tokens:
				ranked_tokens[bigram] += 1
			else:
				ranked_tokens[bigram] = 1
	# pass the tokens based on rank, and also pass the number of posts that were used to achieve this evaluation
	return {'keywords': [d for d in sorted(ranked_tokens.items(), key=lambda item: item[1], reverse=True)], 'notesScanned': len(texts)}

app = Flask(__name__)
CORS(app)
api = Api(app)

# Register the user
keep = gkeepapi.Keep()
keep.login(account['user'], account['password'])

notes = []
def refresh():
	keep.sync()
	gnotes = keep.find(labels=[keep.findLabel('AnneFrank')])
	for note in gnotes:
		notes.append(note)

# Get relevant notes
class Refresh(Resource):
	def get(self):
		refresh()

class HelloWorld(Resource):
	def get(self):
		return {'hello': 'world'}

class Note(Resource):
	def get(self, note_id):
		note = keep.get(note_id)
		score = calcScore(note.text)
		return {
			'title': note.title,
			'text': note.text,
			'score': score, 
			'timestamps': {
				'create': note.timestamps.created.timetuple(),
				'edited': note.timestamps.edited.timetuple()
			}
		}

class Timeline(Resource):
	def get(self):
		# Build an array of {note.title, note.timestamp, note.sentiment, note.link}
		#start_day = (int(start_day[0:4]), int(start_day[4:6]), int(start_day[6:]))
		timeline = []
		for note in notes:
			print(note)
			entry = {
				'id': note.id,
				'timestamp': (int(note.text[0:4]), int(note.text[5:7]), int(note.text[8:10])),
				'title': note.title,
				'score': calcScore(note.text)
			}
			#print( entry['timestamp'], start_day, entry['timestamp'] < start_day)
			#if entry['timestamp'] > start_day:
			timeline.insert(0, entry)
		timeline.sort(key=lambda x: x['timestamp'])
		return timeline

class Keywords(Resource):
	def get(self):
		# Returns an object of keyword:occurences
		return {'positive': getKeyWords(notes[15:22]), 'negative': getKeyWords(notes[15:22], positive=False)}

api.add_resource(HelloWorld, '/')
api.add_resource(Refresh, '/refresh')

api.add_resource(Note, '/notes/<string:note_id>')
api.add_resource(Timeline, '/notes/timeline')
api.add_resource(Keywords, '/notes/keywords')

# Refresh the list
refresh()
test = keep.all()
print(f"Found {len(notes)}/{len(test)} relevant notes")

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)