import json
import os
import logging
import aiofiles
from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)

# Create a view for file uploads
class PersistenceView(HomeAssistantView):
    """Handle JSON persistence via Home Assistant API."""

    url = f'/api/ha_draw_persistence/upload'
    name = 'api:json_data_upload'
    requires_auth = True  # This ensures authentication is required

    def __init__(self, upload_directory):
        self.upload_directory = upload_directory

    async def post(self, request):
        """Handle JSON upload."""
        try:
            # Ensure proper authentication
            hass = request.app['hass']

            # Read multipart data
            data = await request.post()
            json_data = data.get("jsondata")
            file_name = data.get("filename")
            user_name = data.get("user")

            if not file_name:
                return self.json_message("No File Name Provided", status_code=400)

            if not json_data:
                return self.json_message('No json send', status_code=400)

            if not user_name:
                return self.json_message('No User Name Provided', status_code=400)

            try:
                # Attempt to parse to ensure it's valid JSON
                json.loads(json_data)
            except json.JSONDecodeError:
                return self.json_message('Invalid JSON format', status_code=400)

            user_directory = os.path.join(self.upload_directory, user_name)
            os.makedirs(user_directory, exist_ok=True)

            file_path = os.path.join(f"{user_directory}", f"tldraw_persistence_{file_name}.json")

            # Save file
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(json_data)

            _LOGGER.info(f"successfully wrote Json Data: {json_data[:15]}")
            return self.json_message(f'Json Data {json_data[:15]} written successfully')

        except Exception as e:
            _LOGGER.error(f"Json Data error: {e}")
            return self.json_message('Upload failed', status_code=500)

    async def get(self, request):
        """Handle JSON retrieval."""
        hass = request.app['hass']

        try:
            file_name = request.query.get('filename', 'default')
            user_name = request.query.get('user', 'default')

            if not user_name:
                return self.json_message("No User Name Provided", status_code=400)

            if not file_name:
                return self.json_message("No File Name Provided", status_code=400)

            user_directory = os.path.join(self.upload_directory, user_name)
            file_path = os.path.join(f"{user_directory}", f"tldraw_persistence_{file_name}.json")

            # Check if file exists
            if not os.path.exists(file_path):
                return self.json_message('No saved data', status_code=404)

            # Read file asynchronously
            async with aiofiles.open(file_path, 'r') as f:
                json_data = await f.read()

            # Validate JSON before returning
            try:
                json.loads(json_data)
            except json.JSONDecodeError:
                return self.json_message('Stored data is not valid JSON', status_code=500)

            # Return JSON directly
            return self.json(json.loads(json_data))

        except Exception as e:
            _LOGGER.error(f"JSON Data read error: {e}", exc_info=True)
            return self.json_message('Retrieval failed', status_code=500)