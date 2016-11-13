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
PWD_RE=re.compile(r"^.{3,20}$")
EMAIL_RE=re.compile(r"^[\S]+@[\S]+.[\S]+$")

users_list=[]

def valid_username(username):
    return USER_RE.match(username)

def valid_pwd(pwd):
    return PWD_RE.match(pwd)

def valid_email(email):
    return EMAIL_RE.match(email)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **kw):
        t=jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write( self.render_str(template, **kw))

class SignUp(Handler):
    def get(self):
        self.signup_render()

    def post(self):
        name_input= self.request.get("username")
        pwd_input=self.request.get("password")
        pwd2_input=self.request.get("verify")
        email_input=self.request.get("email")

        flag_int=0

        name_notice=""
        name=""
        if name_input!="" and valid_username(name_input):
            name=name_input
            flag_int=flag_int+1

        else:
            name_notice="That's not a valid username."

        pwd=""
        pwd_notice=""
        if pwd_input !="" and valid_pwd(pwd_input):
            pwd=pwd_input
            flag_int=flag_int+1
        else:
            pwd_notice="That was not a valid password."

        pwd2=""
        pwd2_notice=""
        if pwd!="":
            if pwd2_input==pwd_input:
                pwd2=pwd2_input
                flag_int=flag_int+1
            else:
                pwd2_notice="Your passwords didn't match."

        email=""
        email_notice=""
        if (email_input!="" and valid_email(email_input)) \
            or email_input=="" :
            email=email_input
            # flag_int=flag_int+1
        else:
            email_notice="That was not a valid email address."
            flag_int=flag_int-1
            print ("wrong email")

        if flag_int>=3 :
            #redirect url to welcome
            print("welcome")
            users_list.append(name)
            print(users_list)
            self.redirect('/welcome')
        else:
            self.signup_render( \
                        name_notice, \
                        pwd_notice, \
                        pwd2_notice, \
                        email_notice)

    def signup_render(self, name_notice="", pwd_notice="", \
     verify_notice="", email_notice=""):
        self.render("signup.html", \
            name_notice=name_notice, \
            password_notice=pwd_notice, \
            verify_notice= verify_notice, \
            email_notice= email_notice)
    
class Welcome(Handler):
    def get(self):
        self.render("welcome.html", user=users_list[-1])

app = webapp2.WSGIApplication([('/signup', SignUp),
                                ('/welcome', Welcome)
                               ],
                              debug=True)