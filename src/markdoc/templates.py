# -*- coding: utf-8 -*-

import os.path as p

import jinja2
import markdoc
from markdoc.config import Config


Config.register_default('use-default-templates', True)


def build_template_env(config):
    """Build a Jinja2 template environment for a given config."""
    
    load_path = []
    
    if p.isdir(config.template_dir):
        load_path.append(config.template_dir)
    
    if config['use-default-templates']:
        load_path.append(markdoc.default_template_dir)
    
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(load_path))
    environment.globals['config'] = config
    return environment


def template_env(config):
    if not getattr(config, '_template_env', None):
        config._template_env = build_template_env(config)
    return config._template_env

Config.template_env = property(template_env)
