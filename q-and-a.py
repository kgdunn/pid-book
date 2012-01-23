# -*- coding: utf-8 -*-
"""
    Based on the sphinx/ext/ifconfig.py extension code and the extension
    tutorial on the Sphinx website.

    Kevin Dunn, kgdunn@gmail.com, 3-clause BSD license.
    https://bitbucket.org/kevindunn/LINK
"""
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

def boolean_input(argument):
    return directives.choice(argument.lower() , ('yes', 'no')) == 'yes'

class question_answer(nodes.Element): pass

class Question_Answer(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 2
    final_argument_whitespace = True
    option_spec = {'fullinclude': boolean_input,  # include answer? "yes" or "no"
                   'short': directives.unchanged} # short answer?

    def add_content(self):
        node = question_answer()
        node.document = self.state.document
        node.line = self.lineno
        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)
        return node

    def run(self):
        self.assert_has_content()
        env = self.state.document.settings.env

        out = []
        if self.name == 'question':
            # self.src is the full name of the file we are dealing with
            q_number = env.new_serialno(env.docname) + 1
            out.append(nodes.rubric('', 'Question %d' % q_number))
            out.append(self.add_content())

        elif self.name == 'answer':
            # Default value is False (i.e. we obey the 'fullinclude' option)
            override = self.state.document.settings.env.config.q_and_a_override
            if not self.options.has_key('fullinclude') or override:
                # If the option wasn't given, or if the 'q_and_a_override'
                # flag is True
                self.options['fullinclude'] = True
            if self.options['fullinclude']:
                out.append(nodes.paragraph('', ''))
                out.append(nodes.strong('', 'Solution'))
                out.append(nodes.paragraph('', ''))
                out.append(self.add_content())
            elif self.options.get('short', ''):
                out.append(nodes.paragraph('', ''))
                out.append(nodes.strong('', 'Short answer'))
                out.append(nodes.Text(': ' + self.options.get('short')))

        return out

def process_question_nodes(app, doctree, docname):
    ns = app.config.__dict__.copy()
    ns['builder'] = app.builder.name
    for node in doctree.traverse(question_answer):
        node.replace_self(node.children)

def setup(app):
    app.add_directive('question', Question_Answer)
    app.add_directive('answer', Question_Answer)
    app.add_config_value('q_and_a_override', False, False)
    app.connect('doctree-resolved', process_question_nodes)
