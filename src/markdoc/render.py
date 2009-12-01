# -*- coding: utf-8 -*-

from markdoc.config import Config
import markdown


Config.register_default('markdown.extensions', ())
Config.register_func_default('markdown.extension-configs', lambda cfg, key: {})
Config.register_default('markdown.safe-mode', False)
Config.register_default('markdown.output-format', 'xhtml1')
Config.register_default('document-extensions',
    frozenset(['.md', '.mdown', '.markdown', '.wiki', '.text']))


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


def get_markdown_instance(config, **extra_config):
    """Return a `markdown.Markdown` instance for a given configuration."""
    
    mdconfig = dict(
        extensions=config['markdown.extensions'],
        extension_configs=unflatten_extension_configs(config),
        safe_mode=config['markdown.safe-mode'],
        output_format=config['markdown.output-format'])
    
    mdconfig.update(extra_config) # Include any extra kwargs.
    
    return markdown.Markdown(**mdconfig)

# Add it as a method to `markdoc.config.Config`.
Config.markdown = get_markdown_instance
