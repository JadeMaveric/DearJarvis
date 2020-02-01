from flask import Flask
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
sid = SentimentIntensityAnalyzer()

def calcScore(text):
    return sid.polarity_scores(text)

# get a rank of all the keywords depending on their intersections
def getKeyWords(notes, positive=True):
	# step 0: score every note depending on the analysis
	score = [[calcScore(note.text), note.text] for note in notes]
	# step 1: get all of the notes of a specific compound category
	if positive == True:
		texts = [d for d in sorted(score, key=lambda item: item[0]['compound']) if d[0]['compound'] > 0]
	else:
		texts = [d for d in sorted(score, key=lambda item: item[0]['compound']) if d[0]['compound'] < 0]
	# step 2: rank every token in the arrays depending on how common they are...
	# step 2.1: postag and tokenize each text
	# step 2.2: then find intersects and rank accordingly
	tokenized_texts = [nltk.pos_tag(nltk.word_tokenize(text[1])) for text in texts]
	# added a special filter out everything except certain POS tags(i.e only nouns).
	pos_filter = ['NN', 'NNP', 'NNPS', 'NNS']
	ranked_tokens = {}
	for text in tokenized_texts:
		for token in text:
			if token[1] in pos_filter:
				if token in ranked_tokens:
					ranked_tokens[token] += 1
				else:
					ranked_tokens[token] = 1
	# pass the tokens based on rank, and also pass the number of posts that were used to achieve this evaluation
	return [d for d in sorted(ranked_tokens.items(), key=lambda item: item[1])], len(texts)

app = Flask(__name__)
api = Api(app)

# Register the user
keep = gkeepapi.Keep()
keep.login(account['user'], account['password'])

notes = []
def refresh():
    keep.sync()
    gnotes = keep.find(labels=[keep.findLabel('introspect')])
    for note in gnotes:
        notes.append(note)
    print(notes)

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
        timeline = [1, 2, 3]
        print("Notes", notes)
        for note in notes:
            entry = {
                'id': note.id,
                'timestamp': note.timestamps.created.timetuple(),
                'title': note.title,
                'score': calcScore(note.text)
            }
            print(entry)
            print("Hello")
            timeline.insert(0, entry)
        print(timeline)
        return timeline

api.add_resource(HelloWorld, '/')
api.add_resource(Refresh, '/refresh')

api.add_resource(Note, '/notes/<string:note_id>')
api.add_resource(Timeline, '/notes/timeline')

# Refresh the list
refresh()
test = keep.all()
print(f"Found {len(test)} notes")

if __name__ == '__main__':
    app.run(debug=True)