#coding:utf-8

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users
import base64
import urllib,urllib2


class User(db.Model):
  username = db.StringProperty(required = True)
  password = db.StringProperty(required = True)
  email = db.StringProperty(required = True)

class Funcs:
  """处理消息"""

  def saveUser(self, n, p, e):
    #验证用户
    url = 'http://api.fanfou.com/account/verify_credentials.xml'
    encodedstring = base64.encodestring(n + ':' + p)[:-1]
    auth = "Basic %s" % encodedstring
    #mine = 'Basic '+base64.b64encode(n + ':' + p)
    req = urllib2.Request(url, None, {"Authorization":auth})
    response = urllib2.urlopen(req)
    #----不知道会返回什么
    try:
        u = User(username=n, password=p, email=e)
        u.put()
        return '绑定成功'
    except:
        return '绑定失败'

  def save(self, n, p, e):
    results = db.GqlQuery("SELECT * FROM User WHERE email = :1", e)
    if results.count() > 0 :
        for u in results :
            u.delete()
    u = User(username=n, password=p, email=e)
    u.put()

  def getUser(self, e):
    results = db.GqlQuery("SELECT * FROM User WHERE email = :1 LIMIT 1", e)
    flag = False
    for u in results :
        name = u.username
        pwd = u.password
        flag = True
    if flag :
        auth = "Basic " + base64.b64encode(name + ':' + pwd)
        return auth
    else :
        return ''

  def checkUser(self, e):
    results = db.GqlQuery("SELECT * FROM User WHERE email = :1", e)
    if results.count() > 0 :
        u = results[0]
        return u.username
    else :
        return 'Failed'