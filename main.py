import logging

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template

#Models
class Post(db.Model):
  title   = db.StringProperty(required=True)
  content = db.TextProperty(required=True)
  category = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)

#Handlers
class MainHandler(webapp.RequestHandler):
  def get(self):
    query = Post.all()
    if self.request.get("filter"):
      query.filter("category",self.request.get("filter")) 
    posts = query.order("-created").fetch(1000)
    self.response.out.write(template.render('templates/main.html', locals()))

class PostHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render('templates/post_add.html', locals()))

  def post(self):
    title = self.request.get("title")
    category = self.request.get("category")
    content = self.request.get("content")
    logging.info("Salvando un nuevo Post con valores: title: " + title + " content: " + content + " category:" + category)
    post = Post(title=title,content=content,category=category)
    post.put()
    self.redirect("/")

class PostEditHandler(webapp.RequestHandler):
  def get(self,key):
    post = db.get(key)
    self.response.out.write(template.render('templates/post_edit.html', locals()))

  def post(self,key):
    title = self.request.get("title")
    category = self.request.get("category")
    content = self.request.get("content")
    post = db.get(key)
    post.title = title
    post.category = category
    post.content = content
    post.put()
    self.redirect('/')

class PostDeleteHandler(webapp.RequestHandler):
  def get(self,key):
    post = db.get(key)
    self.response.out.write(template.render('templates/post_delete.html', locals()))

  def post(self,key):
    post = db.get(key)
    post.delete()
    self.redirect('/')

def main():
  application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/post/add', PostHandler),
    ('/post/edit/(.+)', PostEditHandler),
    ('/post/delete/(.+)', PostDeleteHandler),
  ], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
