class Note(Resource):
    def get(self, note_id):
        note = keep.get(note_id)
        return note