# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
# Copyright (C) 2025 Northwestern University.
#
# invenio-sitemap is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Views."""


from flask import Blueprint, abort, render_template
from invenio_cache import current_cache

from .cache import SitemapCache, SitemapIndexCache

blueprint = Blueprint(
    "invenio_sitemap",
    __name__,
    template_folder="templates",
    static_folder="static",
)


def _get_cached_or_404(cache_cls, page):
    """Get cached entries or abort to 404 immediately."""
    cache = cache_cls(current_cache)
    data = cache.get(page)
    if data:
        return data
    else:
        abort(404)


@blueprint.route("/sitemap_index_<int:page>.xml", methods=["GET"])
def sitemap_index(page):
    """Get the sitemap index."""
    entries = _get_cached_or_404(SitemapIndexCache, page)
    return render_template(
        "invenio_sitemap/sitemap_index.xml",
        mimetype="text/xml",
        entries=entries,
    )


@blueprint.route("/sitemap_<int:page>.xml", methods=["GET"])
def sitemap(page):
    """Get the sitemap page."""
    entries = _get_cached_or_404(SitemapCache, page)
    return render_template(
        "invenio_sitemap/sitemap.xml",
        mimetype="text/xml",
        entries=entries,
    )
