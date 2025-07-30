import glob
import os
import re
import logging
import sys
import shutil
import nbformat

from traitlets.config import Config
from nbconvert import HTMLExporter
from shutil import copyfile

#TODO add validation and error checking throughout
#TODO cleanup logging
#TODO cleanup return values
#TODO use fname instead of title for dict keys (guarunteed to be different)

class Converter:


    def __init__(self, config_dict, new_nbs=None, existing_nbs=None):
        ''' The converter workhorse '''
        self.conf = config_dict
        self.logger = logging.getLogger(__name__)

        self.new_nbs = new_nbs or self.collect_new_nbs()
        self.existing_nbs = existing_nbs or self.collect_existing_nbs()


    def collect_existing_nbs(self):
        """ Collects existing notebooks from site notebooks folder """
        
        self.logger.debug("Getting existing notebook files: {}".format(self.conf['nb_write_path']))
        
        nb_file_paths = glob.glob(os.path.join(self.conf['nb_write_path'], '*'))
        nb_file_paths.sort()

        self.logger.debug("Found: {}".format(len(nb_file_paths)))
        
        return nb_file_paths


    def collect_new_nbs(self):
        """ Return sorted dictionary of notebooks """

        self.logger.debug("Getting notebook files from {}".format(self.conf['nb_read_path']))

        nb_file_paths = glob.glob(os.path.join(self.conf['nb_read_path'], '*.ipynb'))
        nb_file_paths.sort()

        self.logger.debug("Found: {}".format(len(nb_file_paths)))

        nbs = {}
        for nb_path in nb_file_paths:
            self.logger.debug("\nGathering notebook: {}".format(nb_path))
            
            new_nb = {}
            new_nb['fname'] = nb_path.split("/")[-1][:-6]
            new_nb['skip_build'] = False
            new_nb['read_path'] = self.conf['nb_read_path']
            new_nb['write_path'] = self.conf['nb_write_path']
            new_nb['nbnode'] = self.get_nbnode(nb_path)

            new_nb['body'] = self.get_body(new_nb['nbnode'])
            new_nb['topics'] = self.get_topics(new_nb['nbnode'])
            new_nb['title'] = self.get_title(new_nb['nbnode'])
            new_nb['permalink'] = self.get_permalink(new_nb['title'])

            new_nb['nav'] = None
            new_nb['info'] = "{{site.nb_info}}"

            new_nb['front_matter'] = self.get_front_matter(new_nb['title'], new_nb['permalink'], new_nb['topics'])

            temp = {}
            temp[new_nb['title']] = new_nb
            nbs.update( temp )

        return nbs
    

    def get_summary(self):
        """ Print summary of nbs """

        self.logger.debug('Getting summary...')

        nbs_str = ""
        
        for k in self.new_nbs.keys():
            
            fname = self.new_nbs[k]['fname']

            if self.new_nbs[k]['skip_build']:
                nb_str = "\n\n{} -- SKIPPED".format(fname)
            
            else:
                fm = self.new_nbs[k]['front_matter']
                info = self.new_nbs[k]['info'] or ''
                nav = self.new_nbs[k]['nav'] or ''
                body = '<!--HTML BODY - not shown in preview...too long-->'
                nb_str = "\n\n{}.html\n{}\n{}\n{}\n{}".format(fname, fm, info, nav, body)
            
            nbs_str = nbs_str + nb_str

        return nbs_str

    
    def get_nbnode(self, nb_path):
        """ Returns the nbnode """
        return nbformat.read(nb_path, as_version=4)


    def get_body(self, nb_node):
        """ Get HTML body from notebook and fix links """

        self.logger.debug('Getting nb body...')

        # Setup html exporter template/configs
        html_exporter = HTMLExporter()
        html_exporter.template_file = 'basic'
 
        (body, resources) = html_exporter.from_notebook_node(nb_node)
        fixed_body = self.fix_links(body)
        return fixed_body


    def link_repl(self, matchobj):
        """ Replace src/link matchobj with corrected link """
        print("called repl: {}".format(matchobj.groups()))
        corrected_link = 'src={{{{ "/assets/{}" | relative_url }}}} '.format(matchobj.groups()[0])
        return corrected_link


    def fix_links(self, body):
        """ Find all local asset links and correct """
        s = '|'.join(self.conf['asset_subdirs'])
        regex = re.compile(r'(?:source|src)=\"(\/?(?:%s)\/[\w\d\-_\.]+)\"' % s, re.IGNORECASE)
        fixed_body = re.sub(regex, self.link_repl, body)
        return fixed_body


    def get_title(self, nb_node):
        """ Return notebook title """

        self.logger.debug('Getting nb title...')

        for cell in nb_node.cells:
            if cell.source.startswith('#'):
                title = cell.source[1:].splitlines()[0].strip()
                cleaned_title = re.sub(r'[^\w\s]', '', title)
                break

        return cleaned_title or ''


    def get_permalink(self, nb_title):
        """ Return notebook permalink """

        self.logger.debug('Getting nb permalink...')

        #TODO harden...check for special chars, etc
        permalink = nb_title.lower().replace(" ", "-")

        return permalink


    def get_topics(self, nb_node):
        """ Return notebook topics """

        self.logger.debug('Getting nb topics...')

        txt_src = nb_node.cells[0].source
        regex = r"\*\*Topics\sCovered\*\*([\\n\*\s]+[\w\s]+)+"
        m = re.search(regex, txt_src)

        if m:  # m is None
            if len(m.group()) != 0:
                topics = m.group().replace("**Topics Covered**\n* ", "").split("\n* ")
        else:
            topics = ''

        return str(topics)

    
    def get_nb_nav(self, prev_key=None, next_key=None):
        """ Get html for notebook navigation """
        
        self.logger.debug("Getting nb nav...")

        nav_comment = '<!-- NAV -->'
        prev_nb = ''
        contents = '<a href="{{ "/" | relative_url }}">Contents</a>'
        next_nb = ''

        if prev_key != None:
            prev_title = self.new_nbs[prev_key]['title']
            prev_link = self.new_nbs[prev_key]['permalink']
            prev_nb = '&lt; <a href="{{{{ "{}" | relative_url }}}}">{}</a> | '.format(prev_link, prev_title)

        if next_key != None:
            next_title = self.new_nbs[next_key]['title']
            next_link = self.new_nbs[next_key]['permalink']
            next_nb = ' | <a href="{{{{ "{}" | relative_url }}}}">{}</a> &gt;'.format(next_link, next_title)

        nb_nav = '\n<br><br>{}<p style="font-style:italic;font-size:smaller;">{}{}{}</p>\n'.format(nav_comment, prev_nb, contents, next_nb)
        return nb_nav
    
    
    def add_nb_nav(self):
        """ Add nav to all nbs in the build """

        self.logger.debug("Adding nb nav...")

        build_keys = [k for k in self.new_nbs if not self.new_nbs[k]['skip_build']] 

        for i, curr_nb_key in enumerate(build_keys):
            self.logger.debug("{}".format(self.new_nbs[curr_nb_key]['fname']))
            
            prev_nb_key = build_keys[i - 1] if i > 0 else None
            next_nb_key = build_keys[i + 1] if i < len(build_keys) - 1 else None

            self.new_nbs[curr_nb_key]['nav'] = self.get_nb_nav(prev_nb_key, next_nb_key)

        return True


    def get_front_matter(self, title, permalink, topics):
        """ Return front_matter string """

        self.logger.debug('Getting front matter...')

        layout = "notebook"
        fm = "---\nlayout: {}\ntitle: {}\npermalink: /{}/\ntopics: {}\n---\n".format(layout, title, permalink, topics)
        return fm

    
    def clean_write_dir(self):
        """ Remove files from the write directory in conf """
        
        self.logger.debug("Removing files from write dir...")

        files = glob.glob(os.path.join(self.conf['nb_write_path'], '*'))
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
                self.logger.debug("Removed file: {}".format(f))
            elif os.path.isdir(f):
                shutil.rmtree(f)
                self.logger.debug("Removed directory: {}".format(f))
        
        return True
    
    
    def write_nbs(self):
        """ Write notebooks """
        self.logger.debug("Writing notebooks...")

        for nbtitle, nb in self.new_nbs.items():
            if nb['skip_build']:
                self.logger.debug("Skipped: {}".format(nbtitle))
                continue

            out_path = os.path.join(self.conf['nb_write_path'], nb['fname'] + '.html')
            out_dir = os.path.dirname(out_path)

            if os.path.exists(out_path):
                if self.conf.get('overwrite_existing', True):
                    self.logger.debug(f"Overwriting: {out_path}")
                else:
                    self.logger.debug(f"File exists, skipping: {out_path}")
                    continue
            else:
                self.logger.debug(f"Writing new file: {out_path}")
                # only create dir when its truly new
                os.makedirs(out_dir, exist_ok=True)

            with open(out_path, "w") as file:
                file.write(nb['front_matter'])
                if nb['info']:
                    file.write(nb['info'])
                if self.conf['nb_nav_top']:
                    file.write(nb['nav'])
                file.write(nb['body'])
                if self.conf['nb_nav_bottom']:
                    file.write(nb['nav'])

        return True


    def copy_and_move_assets(self):
        """ Move assets (images, etc) from notebook folder to docs/assets folder """
        #TODO change so it doesn't overwrite by default
        # clean_write_dir should be run first cause it confirms with user
        

        for subdir in self.conf['asset_subdirs']:
            pattern = os.path.join(self.conf['nb_read_path'], subdir, '*')

            self.logger.debug(f"Looking in subdir: {subdir} using glob pattern: {pattern}")
            files = glob.glob(pattern)
            self.logger.debug("Found files: {}".format(files))
            
            for src in files:
                if os.path.isfile(src):
                    fname = os.path.basename(src)
                    fdest = os.path.join(self.conf['asset_write_path'], subdir)
                    os.makedirs(fdest, exist_ok=True)

                    dest_path = os.path.join(fdest, fname)
                    self.logger.debug("Copying file: %s → %s", src, dest_path)
                    copyfile(src, dest_path)

        return True


    def validate_front_matter(self, fm=None):
        """ Validate front_matter """
        #TODO
        return True