#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use as follows:

.. dcl:: R
	:height: 500

	data_file = 'http://openmv.net/file/six-point-board-thickness.csv'

	all.boards <- read.csv(datafile)
	boards <- all.boards[1:100, 2:7]
	head(boards)
	summary(boards)
	boxplot(boards)


.. dcl:: python   <-- this will render with a default height of 600px

    d = dict{'a': 1,
             'b': False}
    print(d)

"""

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive

DEFAULT_CONTROL_HEIGHT = 600

def get_size(d, key):
    if key not in d:
        return str(DEFAULT_CONTROL_HEIGHT) + 'px'
    return str(round(float(d[key].strip('px').strip('%')))) + 'px'


class dcl(nodes.General, nodes.Element): pass

def visit_dcl_node_text(self, node):
    text_to_add = ['[Source code: {}]'.format(node['language'])]
    text_to_add.extend(node['source'])
    self.states[-1].append((-1, '\n'.join(text_to_add)))

def visit_dcl_node_latex(self, node):
    # COPIED FROM: sphinx.writers.latex.LaTeXTranslator.visit_literal_block
    # Slightly tweaked so that the first condition in that copied code is not
    # run here.

    labels = self.hypertarget_to(node)
    if labels and not self.in_footnote:
        self.body.append('\n\\def\\sphinxLiteralBlockLabel{' + labels + '}')

    lang = node.get('language', 'default')
    linenos = node.get('linenos', False)
    highlight_args = node.get('highlight_args', {})
    highlight_args['force'] = node.get('force_highlighting', False)
    if lang is self.builder.config.highlight_language:
        # only pass highlighter options for original language
        opts = self.builder.config.highlight_options
    else:
        opts = {}

    hlcode = self.highlighter.highlight_block(
        node.rawsource, lang, opts=opts, linenos=linenos,
        location=(self.curfilestack[-1], node.line), **highlight_args
    )
    # workaround for Unicode issue
    hlcode = hlcode.replace(u'€', u'@texteuro[]')
    if self.in_footnote:
        self.body.append('\n\\sphinxSetupCodeBlockInFootnote')
        hlcode = hlcode.replace('\\begin{Verbatim}',
                                '\\begin{sphinxVerbatim}')
    # if in table raise verbatim flag to avoid "tabulary" environment
    # and opt for sphinxVerbatimintable to handle caption & long lines
    elif self.table:
        self.table.has_problematic = True
        self.table.has_verbatim = True
        hlcode = hlcode.replace('\\begin{Verbatim}',
                                '\\begin{sphinxVerbatimintable}')
    else:
        hlcode = hlcode.replace('\\begin{Verbatim}',
                                '\\begin{sphinxVerbatim}')
    # get consistent trailer
    hlcode = hlcode.rstrip()[:-14]  # strip \end{Verbatim}
    if self.table and not self.in_footnote:
        hlcode += '\\end{sphinxVerbatimintable}'
    else:
        hlcode += '\\end{sphinxVerbatim}'

    hllines = '\\fvset{hllines={, %s,}}%%' %\
              str(highlight_args.get('hl_lines', []))[1:-1]
    self.body.append('\n' + hllines + '\n' + hlcode + '\n')


def visit_dcl_node_html(self, node):
    """
    <div data-datacamp-exercise data-lang="r" data-height="600px">
        <code data-type="sample-code">

            {{SOURCE CODE HERE}}

        </code>
        <code data-type="solution">
        </code>
        <code data-type="sct">
        </code>
    </div>
    """
    self.body.append('<div data-datacamp-exercise data-lang="{}"'.format(node["language"].lower()))
    self.body.append(' data-height="{}">'.format(node['height']))
    self.body.append('<code data-type="sample-code">')
    self.body.append('\n'.join(node['source']))
    self.body.append('</code><code data-type="solution"></code><code data-type="sct"></code></div>')

def depart_dcl_node(self, node):
    pass

class DataCampLite(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "height": directives.unchanged,
        "codefile": directives.unchanged,  # not used for anything, but for the author to track the original file location
    }

    def run(self):
        self.assert_has_content()
        node = dcl(language = self.arguments[0],
                   source = self.content.data,
                   height = get_size(self.options, "height"))
        node.document = self.state.document
        node.rawsource = '\n'.join(self.content.data)
        node.line = self.lineno
        return [node]

def setup(app):
    app.add_node(dcl,
       html=(visit_dcl_node_html, depart_dcl_node),
       text=(visit_dcl_node_text, depart_dcl_node),
       latex=(visit_dcl_node_latex, depart_dcl_node),
       )
    app.add_directive("dcl", DataCampLite)

    return {'parallel_read_safe': True}