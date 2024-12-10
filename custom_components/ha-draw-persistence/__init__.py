from homeassistant.helpers.http import HomeAssistantView
from homeassistant.helpers.typing import ConfigType
from homeassistant.core import HomeAssistant
import logging

DOMAIN = "ha_draw_persistence"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up File Upload."""
    _LOGGER = logging.getLogger("ha_draw_persistence")
    _LOGGER.info("File Upload view registered")
    print(allowed_file("tldraw.json"))
    return True


def allowed_file(filename):
    """
    Check if the file extension is allowed.

    :param filename: Name of the file to check
    :return: Boolean indicating if file is allowed
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
