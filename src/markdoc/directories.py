# -*- coding: utf-8 -*-

import os.path as p

from markdoc.config import Config


def html_dir(config):
    return p.abspath(p.join(config['meta.root'],
        config.get('html-dir', config['hide-prefix'] + 'html')))


def static_dir(config):
    return p.abspath(p.join(config['meta.root'], config.get('static-dir', 'static')))


def wiki_dir(config):
    return p.abspath(p.join(config['meta.root'], config.get('wiki-dir', 'wiki')))


def temp_dir(config):
    return p.abspath(p.join(config['meta.root'],
        config.get('temp-dir', config['hide-prefix'] + 'tmp')))


def template_dir(config):
    return p.abspath(p.join(config['meta.root'],
        config.get('template-dir', config['hide-prefix'] + 'templates')))


Config.register_default('hide-prefix', '.')
Config.register_default('use-default-static', True)
Config.register_func_default('html-dir', lambda cfg, key: html_dir(cfg))
Config.register_func_default('static-dir', lambda cfg, key: static_dir(cfg))
Config.register_func_default('wiki-dir', lambda cfg, key: wiki_dir(cfg))
Config.register_func_default('temp-dir', lambda cfg, key: temp_dir(cfg))
Config.register_func_default('template-dir', lambda cfg, key: template_dir(cfg))

Config.html_dir = property(html_dir)
Config.static_dir = property(static_dir)
Config.wiki_dir = property(wiki_dir)
Config.temp_dir = property(temp_dir)
Config.template_dir = property(template_dir)
