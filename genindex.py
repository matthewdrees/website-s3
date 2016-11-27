import argparse
import logging
import json
import os
import sys
import shutil
import subprocess
import time

class Config:
    def __init__(self, input_path, year, output_path):
        self.year = year
        self.input_path = input_path
        self.output_path = output_path

    def is_index(self):
        # If the year is an empty string we are creating index.html.
        return self.year == ''

def readJson(jsonRelPath):

    with open(jsonRelPath) as f:
        strJson = f.read()

    return json.JSONDecoder().decode(strJson)

def jsonRelPathKey(jsonRelPath):

    j = readJson(jsonRelPath)
    return time.strptime(j['date'], "%B %d, %Y")

def get_year_post_config_files(year_path):
    post_config_files = []
    for item in os.listdir(year_path):
        if item == '.DS_Store':
            # Ignore .DS_Store folders
            continue

        post_config_file = os.path.join(year_path, item, 'a.json')
        if os.path.isfile(post_config_file):
            logging.debug('Found %s config file' % post_config_file)
            post_config_files.append(post_config_file)
        else:
            logging.error('Did not find %s config file' % post_config_file)

    post_config_files.sort(key=jsonRelPathKey, reverse=True)
    return post_config_files

def get_index_post_config_files(config):
    post_config_files = []
    for item in os.listdir(config.input_path):
        try:
            year = int(item)
            logging.debug("Found year %d" % year)
        except ValueError:
            continue

        year_path = os.path.join(config.input_path, item)
        post_config_files.extend(get_year_post_config_files(year_path))

    post_config_files.sort(key=jsonRelPathKey, reverse=True)
    return post_config_files[0:12]

def get_year_folders(config):
    year_folders = []
    for item in os.listdir(config.input_path):
        if item == ".DS_Store":
            continue
        try:
            year = int(item)
            logging.debug("Found year %d" % year)
            year_folders.append(item)
        except ValueError:
            logging.error("Not a year: %s" % item)
            continue

    year_folders.sort(reverse=True)

    return year_folders

def create_html_file(filename_with_path, post_conf_files):

    logging.info('Creating html file "%s"', filename_with_path)

    html = ['<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="utf-8">',
        '<title>Matt and Cress</title>',
        '<script type="text/javascript" src="masonry.pkgd.js"></script>',
        '<style type="text/css">',

        '<!-- reset -->',
        'html, body, div, span, applet, object, iframe,',
        'h1, h2, h3, h4, h5, h6, p, blockquote, pre,',
        'a, abbr, acronym, address, big, cite, code,',
        'del, dfn, em, img, ins, kbd, q, s, samp,',
        'small, strike, strong, sub, sup, tt, var,',
        'b, u, i, center,',
        'dl, dt, dd, ol, ul, li,',
        'fieldset, form, label, legend,',
        'table, caption, tbody, tfoot, thead, tr, th, td,',
        'article, aside, canvas, details, embed,',
        'figure, figcaption, footer, header, hgroup, ',
        'menu, nav, output, ruby, section, summary,',
        'time, mark, audio, video {',
        '    margin: 0;',
        '    padding: 0;',
        '    border: 0;',
        '    font-size: 100%;',
        '    font: inherit;',
        '    vertical-align: baseline;',
        '}',

        '/* HTML5 display-role reset for older browsers */',
        'article, aside, details, figcaption, figure,',
        'footer, header, hgroup, menu, nav, section {',
        '    display: block;',
        '}',

        'body {',
        '    line-height: 1;',
        '}',
        'ol, ul {',
        '    list-style: none;',
        '}',
        'blockquote, q {',
        '    quotes: none;',
        '}',
        'blockquote:before, blockquote:after,',
        'q:before, q:after {',
        '    content: '';',
        '    content: none;',
        '}',
        'table {',
        '    border-collapse: collapse;',
        '    border-spacing: 0;',
        '}',
        '<!-- end reset, local css -->',
        '',
        'h1 {',
        '    display: block;',
        '    font-size: 2em;',
        '    margin-before: 0.67em;',
        '    margin-after: 0.67em;',
        '    margin-start: 0;',
        '    margin-end: 0;',
        '    font-family: Helvetica;',
        '}',
        'h2 {',
        '    font-size: 20px;',
        '    margin-left: 20px;',
        '    margin-right: 20px;',
        '    font-family: Helvetica;',
        '    font-weight: normal;',
        '    color: #ffffff;',
        '}',
        'hr {',
        '    display: block;',
        '    border-style: inset;',
        '    border-width: 1px;',
        '    margin-bottom: 0;',
        '}',
        'p {',
        '    margin-top: 0;',
        '    margin-left: 0;',
        '    margin-right: 0;',
        '    word-wrap: break-word;',
        '}',
        'span.date { font-style: italic; }',
        '#post_clear {',
        '    clear: both;',
        '}',
        '.grid {'
        '     background: #ffffff;'
        '}',
        '.grid:after {',
        "   content: '';",
        '   display: block;',
        '   clear: both;',
        '   }',
        '.grid-item {',
        '  width: 400px;',
        '  float: left;',
        '  background: #ffffff;',
        '  border: 2px solid #ffffff;',
        '  border-color: hsla(0, 0%, 0%, 0.5);',
        '  margin-top: 10px;',
        '}',
        '</style>',
        '</head>',
        '<body>',
        '<header>',
        '<h1>Matt and Cress</h1>',
        '</header>',
        '<nav>',
        '<a href="index.html">home</a>',
        ]
    
    year_folders = get_year_folders(config)
    for year_folder in year_folders:
        html.append('<a href="%s.html">%s</a>' % (year_folder, year_folder))
      
    html.append('</nav>')
    html.append('<hr/>')
    html.append('''<div class="grid" data-masonry='{ "itemSelector": ".grid-item", "columnWidth": 404, "gutter": 10 }'>''')
    for post_conf_file in post_conf_files:

        logging.debug('Creating grid-item for %s' % post_conf_file)
        
        # content/2013/spring/a.json
        # 2013/spring/
        j = readJson(post_conf_file)
        num_images = len(j["images"])
        logging.debug('num images: %d' % num_images)
        post_rel_dir = os.path.dirname(post_conf_file)
        post_out_dir = post_rel_dir.replace(r'content/', '')

        # Deal with movies.
        splits = post_rel_dir.split('/')
        mp4RelFile = os.path.join(os.path.dirname(post_rel_dir), splits[-1], "%s.mp4" % splits[-1])
        logging.debug('mp4RelFile %s' % mp4RelFile)
        if os.path.exists(mp4RelFile):

            # Get movie info
            out = subprocess.check_output(["ffmpeg2theora",
                                           "--info",
                                           mp4RelFile], universal_newlines=True)
            duration = int(json.JSONDecoder().decode(out)["duration"])
            movie_info = ', <a href="%s/movie.html">%d:%02d video</a>' % (post_out_dir,
                    duration // 60,
                    duration % 60) 
        else:
            movie_info = ''

        logging.debug('movie info: %s' % movie_info)
        html.append('<div class="grid-item">')
        html.append('<a href="%s/index.html"><img src="%s/index.jpg" alt="%s" height=300 width=400/></a>' %
            (post_out_dir, post_out_dir, post_out_dir.replace(r'/',' ')))

        html.append('<p><span class="date">%s</span>, <a href="%s/index.html">%d pics</a>%s</p>' % (j['date'],
             post_out_dir,
             num_images,
             movie_info))

        html.append('<p>%s</p>' % j['blurb'])
        html.append('</div>')
      
    html.append('</div>')
    html.append('</body>')
    html.append('</html>')

    with open(filename_with_path, 'w') as f:
        f.write('\n'.join(html))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Create part of mattandcress.com.')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='verbose')
    parser.add_argument('--input', metavar='input/path', dest='input',
                        help='Input content path.')
    parser.add_argument('--year', metavar='2016', dest='year', default='',
                        help='Create year index file, e.g. 2016.html.')
    parser.add_argument('--output', metavar='output/path', dest='output',
                        help='Output html path.')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    config = Config(args.input, args.year, args.output)

    if config.is_index(): 
        # If index, scan for 12 most recent postings.
        create_html_file(os.path.join(config.output_path,'index.html'),
                         get_index_post_config_files(config))
    else:
        year_path = os.path.join(config.input_path, config.year)
        create_html_file(os.path.join(config.output_path, config.year + '.html'),
                         get_year_post_config_files(year_path))

