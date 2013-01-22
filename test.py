#coding:utf-8

from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
import base64
import urllib,urllib2
from Funcs import Funcs

class XMPPHandler(webapp.RequestHandler):
  def post(self):
    msg = xmpp.Message(self.request.POST)
    b = msg.sender.split('/', 1)
    email = b[0]
    func = Funcs()
    if msg.body[0:5].lower() == '/name':
        a = msg.body.split('=', 2)
        name = a[1]
        pwd = a[2]
        func.save(name, pwd, email)
        msg.reply("已绑定, 因为目前无法验证用户, 输错自负.")
    elif msg.body[0:5].lower() == '/help':
        msg.reply("绑定用户请回复: /name=ID=密码\nID和密码以一个'='间隔, 请不要加入其他字符\n目前无法验证用户, 如有错误请重新绑定, 谢谢!")
        msg.reply("查看目前绑定用户请回复: /see \n如果长时间未回复, 请重新绑定, 谢谢!")
    elif msg.body[0:4].lower() == '/new':
        msg.reply("这里是查看新消息\n目前这里是一片空白")
    elif msg.body[0:4].lower() == '/see':
        res = func.checkUser(email)
        msg.reply(res)
    else:
        msg.reply('然后呢?')
        auth = func.getUser(email)
        if len(auth) > 1 :
            data = msg.body.encode('utf-8')
            url = 'http://api.fanfou.com/statuses/update.xml'
            headers = {"Content-type":"application/x-www-form-urlencoded", "Accept":"text/xml", "Authorization": auth}
            params = urllib.urlencode({"status": data, "source":"then"})
            req = urllib2.Request(url, params, headers)
            response = urllib2.urlopen(req)


application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()