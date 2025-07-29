#     Copyright 2025, GONHXH,  find license text at end of file


""" Cleanup of caches for HxHGoN.

This is triggered by "--clean-cache=" usage, and can cleanup all kinds of
caches and is supposed to run before or instead of HxHGoN compilation.
"""

import os

from Gon.BytecodeCaching import getBytecodeCacheDir
from Gon.Tracing import cache_logger
from Gon.utils.AppDirs import getCacheDir
from Gon.utils.FileOperations import removeDirectory


def _cleanCacheDirectory(cache_name, cache_dir):
    from Gon.Options import shallCleanCache

    if shallCleanCache(cache_name) and os.path.exists(cache_dir):
        cache_logger.info(
            "Cleaning cache '%s' directory '%s'." % (cache_name, cache_dir)
        )
        removeDirectory(
            cache_dir,
            logger=cache_logger,
            ignore_errors=False,
            extra_recommendation=None,
        )
        cache_logger.info("Done.")


def cleanCaches():
    _cleanCacheDirectory("ccache", getCacheDir("ccache"))
    _cleanCacheDirectory("clcache", getCacheDir("clcache"))
    _cleanCacheDirectory("bytecode", getBytecodeCacheDir())
    _cleanCacheDirectory("dll-dependencies", getCacheDir("library_dependencies"))



