"""
CMS Plugins installations
"""
from cms.plugin_pool import plugin_pool

from .plugins.articleflux import ArticleFluxPlugin


# Register plugins
plugin_pool.register_plugin(ArticleFluxPlugin)
