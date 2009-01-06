#!/usr/bin/env python
"""
Python command line client for gist.github.com

Based on Chris Wanstrath's ruby gist client: 
    http://github.com/defunkt/gist/tree/master
    
Usage:
    cat file.txt | pygist
    pygist file1 file2 file3 file4
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
import urllib2

from urllib import urlencode as urlencode

site = 'http://gist.github.com/gists'

def gen_req(files):
    i = 1
    data = []

    for filename in files:
        if filename is sys.stdin:
            ext = '.txt'
            contents = sys.stdin.read()
        else:
            ext = os.path.splitext(filename)[1]
            contents = open(filename).read()

        fname = os.path.basename(filename)

        tmp = {
            'file_ext[gistfile%d]' % i: ext,
            'file_name[gistfile%d]' % i: fname,
            'file_contents[gistfile%d]' % i: contents,
        }
        data.append(urlencode(tmp))
        i += 1

    return ''.join(data)

def get_paste(id):
    url = 'http://gist.github.com/%s.txt' % id
    return urllib2.urlopen(url).read()

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(version=__version__)
    parser.set_usage("%prog [options] [file1 file2 ...]")
    parser.set_description("Python command line client for gist.github.com")
    parser.disable_interspersed_args()
    parser.add_option('-g', dest='gist_id', 
                      help='retreive a paste identified by the gist id')

    opts, args = parser.parse_args()

    if opts.gist_id:
        print get_paste(opts.gist_id)
        sys.exit()

    # Print message with no arguments so users don't think its hung
    if os.isatty(sys.stdin.fileno()) and not args:
        parser.print_help()
        sys.exit()

    if len(args) < 1:
        data = gen_req([sys.stdin])
    else:
        data = gen_req(args)

    info = urllib2.urlopen(site, data)
    print info.geturl()
