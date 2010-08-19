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
from markdown2 import markdown

class FrontPage(webapp.RequestHandler):
    def get(self):
        query = models.Quiz.all().order('-title')
        quizes = []
        for quiz in query.fetch(50):
            quizes.append({'title': markdown_nopara(quiz.title),
                           'link': '/view?key=' + str(quiz.key())})
        template_values = {'quizes': quizes}
        path = os.path.join(os.path.dirname(__file__), 'templates', 'front_page.html')
        self.response.out.write(template.render(path, template_values))

class EditQuiz(webapp.RequestHandler):
    def get(self):
        # FIXME: add optional loading of pre-existing quiz
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'templates', 'edit_quiz.html')
        self.response.out.write(template.render(path, template_values))

class SaveQuiz(webapp.RequestHandler):
    def post(self):
        json_str = self.request.get('json')
        if json_str is None:
            self.error(400)
            self.response.out.write('<h1>Error 400: Quiz data not specified!</h1>')
            return
        data = json.loads(json_str)
        quiz = models.Quiz(title = data['title'],
                           draft = False,
                           content = db.Text(json.dumps(data['questions'])))
        quiz.put()          # Save data in database
        self.redirect('/view?key=' + str(quiz.key()))

class ViewQuiz(webapp.RequestHandler):
    def get(self):
        key_str = self.request.get('key')
        if key_str is None:
            self.error(400)
            self.response.out.write('<h1>Error: Key not specified.</h1>')
            return
        quiz = db.get(db.Key(key_str))
        if quiz is None:
            self.error(404)
            self.response.out.write('<h1>404! No such quiz exists.</h1>')
            return
        template_values = {
            'title': markdown(quiz.title)[3:-5],
            'title_text': quiz.title,
            'questions': process_markdown(json.loads(quiz.content))
            }
        path = os.path.join(os.path.dirname(__file__), 'templates', 'view_quiz.html')
        self.response.out.write(template.render(path, template_values))

#######################
# Markdown processing
#######################

def markdown_nopara(str):
    """Process str as markdown, but remove the <p> and </p> at the
    beginning and end. This is only safe for strings with a single
    paragraph."""
    return markdown(str)[3:-5]

def process_markdown(questions):
    """Process the Markdown in JSON quiz data into HTML. This
    destructively modifies data, so if that's a problem, be sure to
    pass a copy."""
    for question in questions:
        question['question'] = markdown(question['question'])
        for i in range(len(question['answers'])):
            this = question['answers'][i][0]
            question['answers'][i][0] = markdown_nopara(this)
    return questions

##################
# App setup code
##################

application = webapp.WSGIApplication(
                                     [('/', FrontPage),
                                      ('/edit', EditQuiz),
                                      ('/view', ViewQuiz),
                                      ('/do/save_quiz', SaveQuiz)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
