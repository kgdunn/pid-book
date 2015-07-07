#! /usr/bin/env python

import os
import re
import StringIO
import xml.etree.ElementTree as ET
from htmlentitydefs import name2codepoint

ignore_list = ['_images', '_sources', '_static', '.buildinfo', 'contents',
               'index', 'genindex', 'objects.inv', 'search', 'searchindex.js']

shortcut = {
'data-visualization': 'viz',
'data-visualization-exercises': 'viz',
'design-analysis-experiments': 'doe',
'design-analysis-experiments-exercises': 'doe',
'latent-variable-modelling': 'lvm',
'least-squares-exercises': 'reg',
'least-squares-modelling': 'reg',
'process-monitoring': 'mon',
'process-monitoring-exercises': 'mon',
'univariate-exercises': 'univ',
'univariate-review': 'univ',
}

header = re.compile('(?P<prior>.*?)<h1>(?P<sec>\d*).(?P<subsec>\d*).(?P<title>.*?)'
                    '<a class="headerlink" href="(?P<internal>.*?)" '
                    'title="Permalink to this headline">(?P<permalink>.*?)</a></h1>')

htaccess = file('htaccess', 'w')
htaccess.write(u'<IfModule mod_rewrite.c>\n\nRewriteEngine on\n\n')
template = '  RewriteRule ^{0}$\t\t{1}'

baselink = 'http://learnche.org/pid/'
shortner = 'http://yint.org/pid/'

print('Creating permalinks and rewriting the HTML')
for root, dirnames, files in os.walk('_build/html'):
    if len(root.split('/')) > 2:
        if root.split('/')[2] in ignore_list:
            # Skipping this directory
            continue
    for f in files:
        if f in ignore_list:
            # Skipping this file
            continue

        # Do something with this file
        fullpath = os.path.join(root, f)
        with open(fullpath, 'r') as html:
            htmlstr = html.readlines()
        #etree.HTML(''.join(htmlstr))

        with open(fullpath, 'w') as html:
            for line in htmlstr:

                # Find the h1 tags.
                if re.match(header, line):
                    # Modify the line
                    groups = re.match(header, line).groupdict()
                    number = groups['subsec']
                    # Create the shorter link; eg. /pid/vis-1
                    link = shortcut[f] + '-' + number
                    groups['permalink'] = shortner + link + '&nbsp;&nbsp;'

                    # Rewrite the html line for this row
                    line=('{prior}<h1>{sec}.{subsec}.{title}<a class="headerlink" '
                    'href="{internal}" title="Permalink to this headline">'
                    '{permalink}</a></h1>').format(**groups)

                    # Write the .htaccess file
                    # and point it to the longer part, including the #.... anchor
                    htaccess.write(template.format(link,
                            baselink + fullpath[12:] + groups['internal'] + '[NE, L]\n')
                                   )

                # Write the line back to the file
                html.write(line)


htaccess.write(u'</IfModule>\n\n<Files .htaccess>\n  order allow,deny\n  deny from all\n</Files>')
htaccess.close()
print('DONE! Creating permalinks. Remember to copy the .htaccess file.')
