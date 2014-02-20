# -*- coding: utf-8 -*-
"""plone.mls.core API."""

# python imports
import logging

# zope imports
from Acquisition import aq_parent, aq_inner
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone import api
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

# local imports
from plone.mls.core.browser.localconfig import CONFIGURATION_KEY
from plone.mls.core.interfaces import (
    ILocalMLSSettings,
    IMLSSettings,
)


logger = logging.getLogger('plone.mls.core')


def _local_settings(context):
    """Get local MLS settings."""
    settings = None
    obj = context
    while (
            not IPloneSiteRoot.providedBy(obj) and
            not ILocalMLSSettings.providedBy(obj)):
        parent = aq_parent(aq_inner(obj))
        if parent is None:
            return
        obj = parent
    if ILocalMLSSettings.providedBy(obj):
        annotations = IAnnotations(obj)
        settings = annotations.get(
            CONFIGURATION_KEY, annotations.setdefault(CONFIGURATION_KEY, {}))
    return settings


def get_settings(context=None):
    """Get the MLS settings."""
    if context is None:
        context = api.portal.get()

    local_settings = _local_settings(context)
    if local_settings is not None:
        logger.debug('Returning local MLS settings.')
        return local_settings

    # Get the global configuration.
    settings = {}
    registry = getUtility(IRegistry)
    if registry is not None:
        try:
            registry_settings = registry.forInterface(IMLSSettings)
        except:
            logger.warning('Global MLS settings not available.')
        else:
            settings = dict([
                (a, getattr(registry_settings, a)) for a in
                registry_settings.__schema__]
            )
            logger.debug('Returning global MLS settings.')
    return settings
