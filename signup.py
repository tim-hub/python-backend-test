import os
import webapp2
import jinja2
import string
import re

template_dir= os.path.join( \
    os.path.dirname(__file__),'template')
jinja_env=jinja2.Environment( \
    loader=jinja2.FileSystemLoader(template_dir), \
    autoescape=True)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(slef, template, **kw):
        t=jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write( self.render_str(template, **kw))

class SignUp(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):

app = webapp2.WSGIApplication([('/', SignUp),
                               ],
                              debug=True)