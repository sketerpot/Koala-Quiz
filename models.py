##################
# Datastore models
##################

from google.appengine.ext import db

class Quiz(db.Model):
    # The name of the quiz. Something like "Armenian History Quiz 3".
    name = db.StringProperty(required=True)
    # This is true if the quiz is a draft, and should not be displayed
    # publicly.
    draft = db.BooleanProperty(required=True)
    # The user who created the quiz. This is set automatically when
    # the quiz is created.
    creator = db.UserProperty(required=True, auto_current_user_add=True)
    # The content of the quiz itself, represented as a big JSON blob.
    content = db.TextProperty(required=True)
