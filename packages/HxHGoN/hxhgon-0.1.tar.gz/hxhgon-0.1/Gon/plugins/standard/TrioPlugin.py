#     Copyright 2025, GONHXH,  find license text at end of file


""" Deprecated trio plugin.
"""

from Gon.plugins.PluginBase import HxHGoNPluginBase


class HxHGoNPluginTrio(HxHGoNPluginBase):
    plugin_name = "trio"
    plugin_desc = "Deprecated, was once required by the 'trio' package"
    plugin_category = "package-support,obsolete"

    @classmethod
    def isDeprecated(cls):
        return True



