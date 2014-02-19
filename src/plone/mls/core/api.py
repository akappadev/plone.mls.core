# -*- coding: utf-8 -*-
"""plone.mls.core API."""

# python imports
import logging

# zope imports
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# local imports
from plone.mls.core.interfaces import IMLSSettings


logger = logging.getLogger('plone.mls.core')


def _local_settings(context):
    """Get local MLS settings."""
    return None


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
            settings = {
                'agency_id': registry_settings.agency_id,
                'mls_key': registry_settings.mls_key,
                'mls_site': registry_settings.mls_site,
            }
            logger.debug('Returning global MLS settings.')
    return settings
