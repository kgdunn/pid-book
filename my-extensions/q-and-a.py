# -*- coding: utf-8 -*-
"""
    Based on the sphinx/ext/ifconfig.py extension code and the extension
    tutorial on the Sphinx website.

    Kevin Dunn, kgdunn@gmail.com, 3-clause BSD license.
    https://bitbucket.org/kevindunn
"""
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
import hashlib

txt = """ <a class="click-to-reveal" id="{0}-click" href="javascript: void(0);" 
onClick="toggle_q_and_a('{0}')">Click to show answer</a><span id="{0}" class="q_and_a_answer" style="display:none;">"""

def boolean_input(argument):
    return directives.choice(argument.lower() , ('yes', 'no')) == 'yes'

class question_answer(nodes.Element): pass

class Question_Answer(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 2
    final_argument_whitespace = True
    option_spec = {'fullinclude': boolean_input,  # include answer? "yes" or "no"
                   'short': directives.unchanged, # short answer?
                   'copyright_issue': boolean_input,
                  }

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

        # Default value is False (i.e. we obey the 'fullinclude' option)
        override = self.state.document.settings.env.config.q_and_a_override
        # Even include "copyright content" even in "override" mode. 
        # Override literally includes everything:
        already_overridden = False        
        
        out = []
        key = env.docname + 'serialno'
        try:
            current_question = env.temp_data[key]  
        except KeyError:
            # Now we know this is the first time this document is called.
            # Add special HTML to reveal all answers.
            button = '<button id="q_and_a_all" onClick="toggle_all_q_and_a(q_and_a_all)" type="button">Show all answers</button>'
            out.append(nodes.raw('', button, format ='html'))            
            
        if self.name == 'question':
            
            
            if override:
                q_number = env.new_serialno(env.docname) + 1
                if self.state.document.settings.env.app.builder.name == 'html':                    
                    out.append(nodes.raw('', 
                                         '<div class="new_question"></div>', 
                                         format ='html'))                        

                out.append(nodes.rubric(' ', 'Question %d' % q_number))
                out.append(self.add_content())
                already_overridden = True
                
            if self.options.get('copyright_issue'):
                pass
            elif not(already_overridden):
                q_number = env.new_serialno(env.docname) + 1
                if self.state.document.settings.env.app.builder.name == 'html':                    
                    out.append(nodes.raw('', 
                                         '<div class="new_question"></div>', 
                                         format ='html'))                

                out.append(nodes.rubric(' ', 'Question %d' % q_number))
                out.append(self.add_content())
            

        elif self.name == 'answer':
            
            hash_id = hashlib.new('ripemd160')
            
            if not self.options.has_key('fullinclude') or override:
                # If the option wasn't given, or if the 'q_and_a_override'
                # flag is True
                self.options['fullinclude'] = True
                
                # But, also check if there is a copyright issue
                if self.options.get('copyright_issue'):
                    self.options['fullinclude'] = False

            if self.options['fullinclude']:
                out.append(nodes.paragraph(' ', ''))
                out.append(nodes.strong('', 'Solution'))
                
                
                # This code is used below as well
                if self.state.document.settings.env.app.builder.name == 'html':                    
                    hash_id.update(str(current_question))
                    out.append(nodes.raw('', 
                                         txt.format(hash_id.hexdigest()[0:5]), 
                                         format ='html'))          
                # For all output
                out.append(nodes.paragraph(' ', ''))
                out.append(self.add_content())
                
                if self.state.document.settings.env.app.builder.name == 'html':                    
                    out.append(nodes.raw('', '</span>', format ='html'))


            elif self.options.get('short', ''):
                
                out.append(nodes.paragraph('', ''))
                out.append(nodes.strong('', 'Short answer: '))
                
                # This code is used above as well
                if self.state.document.settings.env.app.builder.name == 'html':                    
                    hash_id.update(str(current_question))
                    out.append(nodes.raw('', 
                                         txt.format(hash_id.hexdigest()[0:5]), 
                                         format ='html'))
                    
                out.append(nodes.Text(self.options.get('short')))
                if self.state.document.settings.env.app.builder.name == 'html':                    
                    out.append(nodes.raw('', '</span>', format ='html'))
                
                out.append(nodes.paragraph(' ', ''))

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
    return {'parallel_read_safe': False}