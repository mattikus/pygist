#!/usr/bin/env python
"""
Python command line client for gist.github.com

Based on Chris Wanstrath's ruby gist client: 
    http://github.com/defunkt/gist/tree/master
    
Usage:
    cat file.txt | pygist
    pygist file1 file2 file3 file4
    pygist -p file1
    echo 'hello world' | pygist -a
    pygist -g 1234 > something.txt

"""
__author__ = 'Matt Kemp <matt@mattikus.com>'
__version__ = 'pygist 0.1 1/6/09'
__license__ = """
Copyright (c) 2008 Matt Kemp <matt@mattikus.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import sys
import subprocess
import urllib2

from urllib import urlencode

site = 'http://gist.github.com/gists'

def get_gh_login():
    cmd = subprocess.Popen("which git", shell=True,
                           stdout=subprocess.PIPE).stdout.read().strip()
    if not cmd:
        return

    user = subprocess.Popen(cmd + " config --global github.user", shell=True,
                            stdout=subprocess.PIPE).communicate()[0].strip()
    token = subprocess.Popen(cmd + " config --global github.token", shell=True, 
                             stdout=subprocess.PIPE).communicate()[0].strip()

    return (user, token)

def gen_req(files, private, anon):
    i = 0
    data = {}

    if not anon:
        user, token = get_gh_login()
        if all((user, token)):
            data['login'] = user
            data['token'] = token

        if private:
            data['private'] = 'on'

    for filename in files:
        i += 1
        if filename is sys.stdin:
            ext = ''
            contents = sys.stdin.read()
            fname = ''
        else:
            if not os.path.isfile(filename):
                print "'%s' does not exist or is not a regular file" % filename
                sys.exit()
            ext = os.path.splitext(filename)[1]
            contents = open(filename).read()
            fname = filename

        data['file_ext[gistfile%d]' % i] = ext
        data['file_name[gistfile%d]' % i] = fname
        data['file_contents[gistfile%d]' % i] = contents


    return urlencode(data)

def get_paste(id):
    url = 'http://gist.github.com/%s.txt' % id
    return urllib2.urlopen(url).read()

def copy_paste(url):
    cmd = ''
    if sys.platform == 'darwin':
        cmd = subprocess.Popen('which pbcopy', shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().strip()
    if 'linux' in sys.platform:
        cmd = subprocess.Popen('which xclip', shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().strip()
    if cmd:
        output = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
        output.stdin.write(url)
        output.stdin.close()

    return url
if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(version=__version__)
    parser.set_usage("%prog [options] [file1 file2 ...]")
    parser.set_description("Python command line client for gist.github.com")
    parser.disable_interspersed_args()
    parser.add_option('-g', dest='gist_id', 
                      help='retreive a paste identified by the gist id')
    parser.add_option('-p', dest='private', action='store_true',
                      help='set for private gist')
    parser.add_option('-a', dest='anon', action='store_true',
                      help='set for anonymous gist')

    opts, args = parser.parse_args()

    if opts.gist_id:
        print get_paste(opts.gist_id)
        sys.exit()

    # Print message with no arguments so users don't think its hung
    if os.isatty(sys.stdin.fileno()) and not args:
        parser.print_help()
        sys.exit()

    if len(args) < 1:
        data = gen_req([sys.stdin], opts.private, opts.anon)
    else:
        data = gen_req(args, opts.private, opts.anon)

    info = urllib2.urlopen(site, data)
    print copy_paste(info.geturl())
