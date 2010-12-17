# -*- coding: utf-8 -*-
"""
    Based on the sphinx/ext/ifconfig.py extension code and the extension
    tutorial on the Sphinx website.

    Kevin Dunn, kgdunn@gmail.com, 3-clause BSD license.
    https://bitbucket.org/kevindunn/LINK
"""
from docutils import nodes
from sphinx.util.compat import Directive

class question_answer(nodes.Element): pass

class Question_Answer(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    def run(self):
        env = self.state.document.settings.env
        if self.name == 'question':
            # self.src is the full name of the file we are dealing with
            q_number = env.new_serialno(env.docname) + 1
            title = nodes.rubric('', 'Question %d' % q_number)
        elif self.name == 'answer':
            title = nodes.emphasis('', 'Answer')  # Add a new paragraph here first!
        node = question_answer()
        node.document = self.state.document
        node.line = self.lineno
        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)
        return [title, node]

def process_question_nodes(app, doctree, docname):
    ns = app.config.__dict__.copy()
    ns['builder'] = app.builder.name
    for node in doctree.traverse(question_answer):
        node.replace_self(node.children)

def setup(app):
    app.add_directive('question', Question_Answer)
    app.add_directive('answer', Question_Answer)
    app.connect('doctree-resolved', process_question_nodes)
