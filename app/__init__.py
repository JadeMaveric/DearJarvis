from flask import Flask
from flask_restful import Resource, Api
import gkeepapi

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

account = {
	user: 'introspecthack@gmail.com',
	password: 'Kyjus2020',
}

vectorizer = TfidfVectorizer()
def getKeyWords(notes):
	corpus = []
	for note in notes:
		corpus.append(note.text) 
	model = vectorizer.fit_transform(corpus)
	return vectorizer.get_feature_names(), model	# also returns model

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def calcScore(text):
    return sid.polarity_scores(text)

app = Flask(__name__)
api = Api(app)

# Register the user
keep = gkeepapi.Keep()
keep.login(account.user, account.password)

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