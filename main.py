from ams_crawler import bug
from tornado import web, ioloop, httpserver, options
from tornado.options import define, options

#定义端口
define("port", default=8080, help="run on the given port ", type=int)
define("log_path", default='/tmp', help="log path ", type=str)





#业务模块
class LoginPageHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        if not self.get_cookie("login"):
            self.render("login.html")
        else:
            self.redirect("/Grade_Page")
class GradePageHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
            user_name = self.get_argument("User_Name")
            password = self.get_argument("Password")
            self.set_cookie("login", str(user_name) + "&&&" + str(password), expires_days=30)
            result = bug(user_name, password)
            if result == "invalid login":
                self.redirect("/loginfail")
            else:
                self.render("gradepage.html", CourseAmount=result[0], GPA=result[1], GPACourse=result[2], GPACourseGrade=result[3], Details=result[4])
    def get(self, *args, **kwargs):
        if not self.get_cookie("login"):
            self.redirect("/")
        else:
            cookie = self.get_cookie("login")
            user_name = cookie.split("&&&")[0]
            password = cookie.split("&&&")[1]
            result = bug(user_name, password)
            if result == "invalid login":
                self.redirect("/loginfail")
            else:
                self.render("gradepage.html", CourseAmount=result[0], GPA=result[1], GPACourse=result[2], GPACourseGrade=result[3], Details=result[4])
class tosPageHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("tos.html")
class LogoutPageHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        if not self.get_cookie("login"):
            self.redirect("/")
        else:
            self.clear_cookie("login")
            self.redirect("/")
class LoginfailPageHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie("login")
        self.render("loginfail.html")
class BaseHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write_error(404)
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            self.render('unknown.html')

settings = {
    "template_path": "templates",
    "static_path": "static"
}

#路由系统
application = web.Application([
            (r"/", LoginPageHandler),
            (r"/Grade_Page", GradePageHandler),
            (r"/tos.html", tosPageHandler),
            (r"/logout", LogoutPageHandler),
            (r"/loginfail", LoginfailPageHandler),
            (r".*", BaseHandler)
        ], **settings)




if __name__ == '__main__':
#socket server

        http_server = httpserver.HTTPServer(application)
        http_server.listen(options.port)
        ioloop.IOLoop.current().start()