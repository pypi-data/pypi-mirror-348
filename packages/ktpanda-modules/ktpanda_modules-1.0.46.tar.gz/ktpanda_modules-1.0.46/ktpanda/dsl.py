# dsl.py
#
# Copyright (C) 2025 Katie Rust (katie@ktpanda.org)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
dsl
===

Utility class for implementing a Python-based DSL
'''

import ast
from pathlib import Path

def export(f):
    f._dsl_is_export = True
    return f

class DSL:
    self_name = None

    def __init__(self):
        self.modname = None

        self.globs = dict(
            __file__ = None,
            include_py = self.include_py,
        )

        if self.self_name is not None:
            self.globs[self.self_name] = self

        for ctype in type(self).__mro__:
            for key, val in ctype.__dict__.items():
                if getattr(val, '_dsl_is_export', False):
                    self.globs[key] = val.__get__(self)

    def transform(self, path, tree):
        return tree

    def define_globs(self, **kw):
        self.globs.update(kw)

    def include_py(self, path):
        current_file = self.globs['__file__']
        self.exec_py(Path(current_file).parent / path)

    def exec_py(self, path):
        current_file = self.globs['__file__']
        self.globs['__file__'] = str(path)

        # Read the source and parse it
        py_text = path.read_text('utf8').replace('\r\n', '\n').removeprefix('\ufeff')
        tree = ast.parse(py_text, str(path))
        newtree = ast.fix_missing_locations(self.transform(path, tree))
        exec(compile(newtree, str(path), 'exec'), self.globs)

        self.globs['__file__'] = current_file
