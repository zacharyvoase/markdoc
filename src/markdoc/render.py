# -*- coding: utf-8 -*-

from markdoc.config import Config
import markdown


Config.register_default('markdown.extensions', ())
Config.register_func_default('markdown.extension-configs', lambda: {})
Config.register_default('markdown.safe-mode', False)
Config.register_default('markdown.output-format', 'xhtml1')


def get_markdown_instance(config, **extra_config):
    """Return a `markdown.Markdown` instance for a given configuration."""
    
    mdconfig = dict(
        extensions=config['markdown.extensions'],
        extension_configs=config['markdown.extension-configs'],
        safe_mode=config['markdown.safe-mode'],
        output_format=config['markdown.output-format'])
    
    mdconfig.update(extra_config) # Include any extra kwargs.
    
    return markdown.Markdown(**mdconfig)

# Add it as a method to `markdoc.config.Config`.
Config.markdown = get_markdown_instance
