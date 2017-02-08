#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2;
import os;
import jinja2;
from google.appengine.ext import db;

templateDir = os.path.join(os.path.dirname(__file__), 'templates');
jinjaEnv = jinja2.Environment(loader = jinja2.FileSystemLoader(templateDir), autoescape = True);

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw);

    def renderStr(self, template, **params):
        t = jinjaEnv.get_template(template);
        return t.render(params);

    def render(self, template, **kw):
        self.write(self.renderStr(template, **kw));

class Blog(db.Model):
    title = db.StringProperty(required = True);
    body = db.TextProperty(required = True);
    created = db.DateTimeProperty(auto_now_add = True);

class MainHandler(Handler):

    def get(self):
        self.redirect('/blog'); #automatic redirect to /blog

class BlogHandler(Handler):

    def renderFront(self, title = "", body = ""):
        blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC LIMIT 5');

        self.render('front.html', title = title, body = body, blogs = blogs);

    def get(self):
        self.renderFront();

class NewPost(Handler):
    def get(self):
        self.render('newpost.html', title = '', body = '', error = '');

    def post(self):
        title = self.request.get('title');
        body = self.request.get('body');

        if title and body:
            blog = Blog(title = title, body = body);
            blog.put();
            self.redirect('/blog');
        else:
            error = "New posts require a body and a title"
            self.render('newpost.html', title = title, body = body, error = error);


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogHandler),
    ('/blog/newpost', NewPost),
], debug=True)
