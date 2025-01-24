import json
import os
import logging
import aiofiles
from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)

# Create a view for file uploads
class FileView(HomeAssistantView):
    """Handle get all FileNames via Home Assistant API."""

    url = f'/api/ha_draw_persistence/files'
    name = '/api/ha_draw_persistence/files'
    requires_auth = True  # This ensures authentication is required

    def __init__(self, upload_directory):
        self.upload_directory = upload_directory

    async def get(self, request):
        """"Handels getting all the file names"""

        hass = request.app['hass']

        fileNames = []

        try:
            user_name = request.query.get('user', 'default')

            if not user_name:
                return self.json_message("No User Name Provided", status_code=400)



        except Exception as e:
            _LOGGER.error(f"FileName read error: {e}", exc_info=True)
            return self.json_message('FileName Retrieval failed', status_code=500)