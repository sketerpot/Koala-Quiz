from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app, login_required
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.api.labs import taskqueue
from google.appengine.ext.webapp import template
from django.utils import simplejson as json
import logging, os, sys
import models

class FrontPage(webapp.RequestHandler):
    def get(self):
        # FIXME: list all non-draft quizzes, and have a button to make
        # a new quiz. Use templates.
        self.response.out.write("ORGANS IN MAINS")

class EditQuiz(webapp.RequestHandler):
    def get(self):
        # FIXME: add optional loading of pre-existing quiz
        template_values = {
            'name': 'Joe-Jim'
            }
        path = os.path.join(os.path.dirname(__file__), 'templates', 'edit_quiz.html')
        #self.response.out.write(path)
        self.response.out.write(template.render(path, template_values))


##################
# App setup code
##################

application = webapp.WSGIApplication(
                                     [('/', FrontPage),
                                      ('/edit', EditQuiz)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
