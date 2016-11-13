import os
import webapp2
import jinja2
import string

template_dir= os.path.join( \
    os.path.dirname(__file__),'template')
jinja_env=jinja2.Environment( \
    loader=jinja2.FileSystemLoader(template_dir), \
    autoescape=True)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(slef, template, **kw):
        t=jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write( self.render_str(template, **kw))

class Rot13(Handler):
	def rot13_tran(self, str):
		# new_content= string.maketrans( 
		#     "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
		#     "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
		new_content=str.encode('rot13')
		return new_content

	def get(self):
		self.render("rot13.html")

	def post(self):
		original_content=self.request.get("text")
		new_content=self.rot13_tran(original_content)
		self.render("rot13.html", \
			new_content=new_content )

class SignUp(Handler):
	def get(self):
		self.render("signup.html")

	

app = webapp2.WSGIApplication([('/', Rot13),],
                              debug=True)