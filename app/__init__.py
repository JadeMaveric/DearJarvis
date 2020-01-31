from flask import Flask
from flask_restful import Resource, Api
import gkeepapi

account = {
	user: 'introspecthack@gmail.com',
	password: 'Kyjus2020',
}

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
def getKeyWords(notes):
	corpus = []
	for note in notes:
		corpus.append(note.text) 
	model = vectorizer.fit_transform(corpus)
	return vectorizer.get_feature_names(), model	# also returns model

from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

app = Flask(__name__)
api = Api(app)

# Register the user
keep = gkeepapi.Keep()
keep.login(account.user, account.password)

# Get relevant notes
class Refresh(Resource):
    def get():
        keep.sync()
        gnotes = keep.find(labels=[keep.findLabel('introspect')])
        notes = []
        for note in notes:
            notes.append(note)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Note(Resource):
    def get(self, note_id):
        note = keep.get(note_id)
        # Run NLP Sentiment analysis on note, give it a score
        score = sid.polarity_score(text)
        return {
            'title': note.title,
            'text': note.text,
            'score': score, 
            'timestamps': {
                'create': note.timestamps.created.timetuple(),
                'edited': note.timestamps.edited.timetuple()
            }
        }

api.add_resource(HelloWorld, '/')
api.add_resource(Note, '/notes/<string:note_id>')
api.add_resource(Refresh, '/refresh')

if __name__ == '__main__':
    app.run(debug=True)