# coding=utf-8

from csearch import CSearch
import tornado.ioloop
import tornado.web
import os
import time


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, world")


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        regexp = self.get_argument('regexp', default='')
        file_regexp = self.get_argument('file_regexp', default='')
        if regexp:
            cs = CSearch()

            cs.search_file(regexp, file_regexp)

            self.render("index.html",  rst_list=cs.rst_list)

        else:
            self.render("index.html",  rst_list=[])


class AddHandler(tornado.web.RequestHandler):

    def get_file_name(self, code_type, filename):
        if not filename:
            filename = str(time.time())
        _dir = self.settings["csearch_path"]
        tag_file_name = self.settings["csearch_tag_file"]
        tag_file_full_name = _dir + '/' + tag_file_name

        full_file_name = _dir + '/' + code_type + '/' + filename

        return tag_file_full_name, full_file_name

    def post(self):
        _type = self.get_argument('type')
        _tags = self.get_argument('tags')
        _code = self.get_argument('code')
        _filename = self.get_argument('filename')
        if not _code.strip():
            self.render("index.html",  rst_list=[])
            return
        tag_file_full_name, full_file_name = self.get_file_name(
            _type, _filename)
        print _type, _tags, _code, _filename,
        tag_file_full_name, full_file_name

        with open(full_file_name, 'aw') as file:
            file.write('%s\n' % _code.encode('utf8'))
            file.flush()
        with open(tag_file_full_name, 'a') as file:
            buff = '%s-%s-%s\n' % (_type, _tags, full_file_name)
            file.writelines(buff.encode('utf8'))
            file.flush()

        cs = CSearch()
        cs.index()
        self.write('It is ok')


class FileHandler(tornado.web.RequestHandler):

    def get(self):
        file_name = self.get_argument("filename")
        with open(file_name, 'r') as file:
            code = file.read()
            # self.render('file.html',code=markdown2.markdown(`code`))
            self.render('file.html', code=code)


settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "csearch_path": '/u01/cdata',
    "csearch_tag_file": 'tags.data'
}

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/index", IndexHandler),
    (r"/add", AddHandler),
    (r"/file", FileHandler)
], **settings)
if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
