# -*- coding: utf-8 -*-

import os.path as p

from markdoc.config import Config
import markdown


Config.register_default('markdown.extensions', ())
Config.register_func_default('markdown.extension-configs', lambda cfg, key: {})
Config.register_default('markdown.safe-mode', False)
Config.register_default('markdown.output-format', 'xhtml1')
Config.register_default('document-extensions',
    frozenset(['.md', '.mdown', '.markdown', '.wiki', '.text']))


class RelativeLinksTreeProcessor(markdown.treeprocessors.Treeprocessor):
    
    """A Markdown tree processor to relativize wiki links."""
    
    def __init__(self, curr_path='/'):
        self.curr_path = curr_path
    
    def make_relative(self, href):
        return make_relative(self.curr_path, href)
    
    def run(self, tree):
        links = tree.getiterator('a')
        for link in links:
            if link.attrib['href'].startswith('/'):
                link.attrib['href'] = self.make_relative(link.attrib['href'])
        return tree


def make_relative(curr_path, href):
    """Given a current path and a href, return an equivalent relative path."""
    
    curr_list = curr_path.lstrip('/').split('/')
    href_list = href.lstrip('/').split('/')
    
    # How many path components are shared between the two paths?
    i = len(p.commonprefix([curr_list, href_list]))
    
    rel_list = (['..'] * (len(curr_list) - i - 1)) + href_list[i:]
    if not rel_list or rel_list == ['']:
        return './'
    return '/'.join(rel_list)


def unflatten_extension_configs(config):
    """Unflatten the markdown extension configs from the config dictionary."""
    
    configs = config['markdown.extension-configs']
    
    for key, value in config.iteritems():
        if not key.startswith('markdown.extension-configs.'):
            continue
        
        parts = key[len('markdown.extension-configs.'):].split('.')
        extension_config = configs
        for part in parts[:-1]:
            extension_config = extension_config.setdefault(part, {})
        extension_config[parts[-1]] = value
    
    return configs


def get_markdown_instance(config, curr_path='/', **extra_config):
    """Return a `markdown.Markdown` instance for a given configuration."""
    
    mdconfig = dict(
        extensions=config['markdown.extensions'],
        extension_configs=unflatten_extension_configs(config),
        safe_mode=config['markdown.safe-mode'],
        output_format=config['markdown.output-format'])
    
    mdconfig.update(extra_config) # Include any extra kwargs.
    
    md_instance = markdown.Markdown(**mdconfig)
    md_instance.treeprocessors['relative_links'] = RelativeLinksTreeProcessor(curr_path=curr_path)
    return md_instance

# Add it as a method to `markdoc.config.Config`.
Config.markdown = get_markdown_instance
