#-*-coding:utf-8-*-

import os
import tornado.web
import tornado.wsgi
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import LISTEN_PORT, DEBUG
from module.models import engine
from handler.admin import *
from handler.content import *
from handler.error import NotFoundHandler

urls = [(r"/", MainHandler),
        (r"/admin/home", AmdinHomeHandler),
        (r"/admin/login", AmdinLoginHandler),
        (r"/admin/logout", AmdinLogoutHandler),
        (r"/admin/setting", AmdinSettingHandler),
        (r"/admin/profile", AmdinProfileHandler),
        (r"/admin/page/list", AmdinPageListHandler),
        (r"/admin/page/add", AmdinPageAddHandler),
        (r"/admin/page/delete/([0-9]+)", AmdinPageDeleteHandler),
        (r"/admin/page/edit/([0-9]+)", AmdinPageEditHandler),
        (r"/admin/post/list", AmdinPostListHandler),
        (r"/admin/post/add", AmdinPostAddHandler),
        (r"/admin/post/delete/([0-9]+)", AmdinPostDeleteHandler),
        (r"/admin/post/edit/([0-9]+)", AmdinPostEditHandler),
        (r"/admin/category/list", AmdinCategoryListHandler),
        (r"/admin/category/add", AmdinCategoryAddHandler),
        (r"/admin/category/quickadd", AmdinCategoryQuickAddHandler),
        (r"/admin/category/delete/([0-9]+)", AmdinCategoryDeleteHandler),
        (r"/admin/category/edit/([0-9]+)", AmdinCategoryEditHandler),
        (r"/category/list", CategoryListHandler),
        (r"/post/category/(.+)/$", PostByCategoryName),
        (r"/post/tag/(.+)/$", PostByTagName),
        (r"/post/id/([0-9]+)", PostById),
        (r"/post/page/([0-9]+)", PostByPageId),
        (r"/comment/add", CommentAddHandler),
        (r"/comment/list", CommentListByPostIdHandler),
        (r"/tag/list", TagListHandler),
        (r".*", NotFoundHandler)]

settings = dict(
            blog_title=u"Lee Blog",
            template_path=(os.path.join(os.path.dirname(__file__), "templates")),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="66oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/admin/login",
            debug=DEBUG,
        )

class WsgiApplication(tornado.wsgi.WSGIApplication):
    def __init__(self):
        tornado.wsgi.WSGIApplication.__init__(self, urls, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = scoped_session(sessionmaker(bind=engine))

