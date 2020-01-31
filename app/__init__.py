from flask import Flask
from flask_restful import Resource, Api
import gkeepapi

app = Flask(__name__)
api = Api(app)

# Register the user
keep = gkeepapi.Keep()
keep.login('introspecthack@gmail.com', 'Kyjus2020')

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
        return {
            'title': note.title,
            'text': note.text,
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