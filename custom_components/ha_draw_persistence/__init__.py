"""
Custom component for file upload in Home Assistant
Place this in your custom_components/ha_draw_persistence/ directory
"""
import json
import os
import logging
import aiofiles
from homeassistant.components.http import HomeAssistantView

from custom_components.ha_draw_persistence.PersistenceView import PersistenceView

DOMAIN = "ha_draw_persistence"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the file upload component."""
    conf = config.get(DOMAIN, {})
    upload_directory = conf.get('upload_directory')

    if not conf:
        _LOGGER.error("Configuration for %s is missing", DOMAIN)
        return False

    # Ensure upload directory exists
    os.makedirs(upload_directory, exist_ok=True)

    hass.data[DOMAIN] = {
        "upload_directory": upload_directory,
    }

    # Register the view
    hass.http.register_view(PersistenceView(upload_directory))

    return True