# coding=utf-8

import subprocess
import os


class SearchResult(object):

    def __init__(self, seq, file_full_name, row_num, file_buff):
        self.seq = '[' + str(seq) + ']'
        self.file_full_name = file_full_name
        self.file_buff = file_buff
        self.row_num = row_num
        self.file_name = os.path.basename(self.file_full_name)

    def to_string(self):
        return ' : '.join([self.seq, self.file_full_name,
                           self.row_num, self.file_buff, self.file_name])


class CSearch(object):

    def __init__(self):
        self.rst_list = list()

    def index(self, folder_list=''):
        self.run_command('cindex', ' '.join(folder_list))

    def reset(self):
        self.run_command('cindex -reset')

    def list(self):
        self.run_command('cindex -list')

    def search(self, regexp, file_regexp=None):
        file_args = ' '
        if file_regexp:
            file_args = '-f ' + file_regexp

        self.run_command(
            'csearch -i -n', file_args, regexp, call_back=self.handler_rst)

    def search_file(self, regexp, file_regexp=None, size=15):
        file_args = ' '
        if file_regexp:
            file_args = '-f ' + file_regexp

        self.run_command(
            'csearch -i -l', file_args, regexp, call_back=self.handler_rst)

    def show(self):
        for rst in self.rst_list:
            print rst.to_string()

    def handler_rst(self, p):
        rf, ef = p.stdout, p.stderr
        self.rst_list = list()

        i = 0
        while True:
            i += 1
            buff = rf.readline()

            if buff == '' and p.poll() != None:
                break
            if buff:
                b = buff.split(':')
                sr = SearchResult(i, b[0], ''.join(b[1:2]), ':'.join(b[2:]))
                self.rst_list.append(sr)
        while True:
            buff = ef.readline()
            if buff == '' and p.poll() != None:
                break
            if buff:
                i += 1
                b = buff.split(':')

                sr = SearchResult(i, b[0], ''.join(b[1:2]), ':'.join(b[2:]))
                self.rst_list.append(sr)

        self.show()

    def default_handler_rst(self, p):
        rf, ef = p.stdout, p.stderr
        print rf.read(),  ef.read()

    def add_file(self):
        self.run_command('vim ', '/u01/data/file')

    def run_command(self, cmd, *args, **kw):
        if not cmd:
            return ''
        if args:
            cmd = ' '.join((cmd,) + args)

        print cmd
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        call_back = kw.get('call_back', '')
        if call_back:
            call_back(p)
        else:
            self.default_handler_rst(p)


def main():
    cs = CSearch()
    cs.search_file('n')

if __name__ == '__main__':
    main()
