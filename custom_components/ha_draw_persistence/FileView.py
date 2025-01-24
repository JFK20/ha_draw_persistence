import os
import logging
import pathlib

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

            user_directory = os.path.join(self.upload_directory, user_name)

            user_directory = pathlib.Path(str(user_directory))

            if not os.path.exists(user_directory):
                return self.json_message("User directory does not exist", status_code=404)

            # List all files in the user directory
            file_names = os.listdir(user_directory)

            return self.json({"files": file_names})


        except Exception as e:
            _LOGGER.error(f"FileName read error: {e}", exc_info=True)
            return self.json_message('FileName Retrieval failed', status_code=500)